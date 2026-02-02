from src.data import load_opsd_de_load

def main():
    df = load_opsd_de_load()

    print("=== DATAFRAME INFO ===")
    print(df.info())

    print("\n=== FIRST 10 ROWS ===")
    print(df.head(10))

    print("\n=== COLUMN NAMES ===")
    print(df.columns)

    print("\n=== INDEX TYPE ===")
    print(type(df.index))

if __name__ == "__main__":
    main()
