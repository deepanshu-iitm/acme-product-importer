from .celery_app import celery_app
from .db_session import get_session
from .models import Product
from .utils import normalize_sku
import csv
import os

def write_batch(session, batch):
    """Insert or update products in a single batch."""

    created = 0
    updated = 0

    batch_map = {}
    for item in batch:
        sku_norm = item["sku_norm"]
        batch_map[sku_norm] = item  
    
    deduplicated_batch = list(batch_map.values())
    
    sku_norms = [item["sku_norm"] for item in deduplicated_batch]

    existing_products = (
        session.query(Product)
        .filter(Product.sku_norm.in_(sku_norms))
        .all()
    )

    existing_map = {p.sku_norm: p for p in existing_products}

    items_to_insert = []


    for item in deduplicated_batch:
        sku_norm = item["sku_norm"]

        if sku_norm in existing_map:
            p = existing_map[sku_norm]
            p.sku = item["sku"]
            p.name = item["name"]
            p.description = item["description"]
            p.price = item["price"]
            updated += 1
        else:
            items_to_insert.append(item)

    if updated > 0:
        session.commit()

    for item in items_to_insert:
        new_product = Product(
            sku=item["sku"],
            sku_norm=item["sku_norm"],
            name=item["name"],
            description=item["description"],
            price=item["price"],
            active=True,            
        )
        session.add(new_product)
        created += 1

  
    if created > 0:
        session.commit()

    return created, updated


def import_csv_to_db(file_path, batch_size=1000):
    """Reads CSV, normalizes, updates/inserts in batches."""

    session = get_session()

    try:
        print("[IMPORT] Starting CSV import:", file_path)

        created = 0
        updated = 0
        batch = []

        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                sku = (row.get("sku") or row.get("SKU") or "").strip()
                name = row.get("name") or ""
                description = row.get("description") or ""
                price_raw = row.get("price") or ""

                # Convert price safely
                try:
                    price = float(price_raw) if price_raw != "" else None
                except Exception:
                    price = None

                # Normalize SKU (lowercase, strip)
                sku_norm = normalize_sku(sku)
                if not sku_norm:
                    continue  # skip invalid rows

                # Append to batch
                batch.append({
                    "sku": sku,
                    "sku_norm": sku_norm,
                    "name": name,
                    "description": description,
                    "price": price,
                })

                # If batch full -> write to DB
                if len(batch) >= batch_size:
                    c, u = write_batch(session, batch)
                    created += c
                    updated += u
                    batch = []

        # leftover rows
        if batch:
            c, u = write_batch(session, batch)
            created += c
            updated += u

        print(f"[IMPORT] Completed. created={created}, updated={updated}")
        return {"created": created, "updated": updated}

    except Exception as e:
        print("[IMPORT] ERROR:", e)
        return {"error": str(e)}

    finally:
        session.close()


# CELERY TASK WRAPPER

@celery_app.task(bind=True)
def import_csv_task(self, file_path, batch_size=1000):
    file_path = os.path.abspath(file_path)
    return import_csv_to_db(file_path, batch_size=batch_size)


@celery_app.task
def add_numbers(a, b):
    return a + b

@celery_app.task
def process_csv(file_path):
    """Legacy test function — optional to keep."""
    import time
    row_count = 0
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            row_count += 1
            time.sleep(0.001)
    return {"rows": row_count}
