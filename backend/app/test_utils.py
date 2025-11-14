from utils import normalize_sku

def test_normalize():
    print(normalize_sku("  ABC123  "))       # expected: "abc123"
    print(normalize_sku("AbC-DeF"))          # expected: "abc-def"
    print(normalize_sku("   "))              # expected: ""
    print(normalize_sku("XYZ"))              # expected: "xyz"

if __name__ == "__main__":
    test_normalize()
