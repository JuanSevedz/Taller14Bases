from datos import conteos, ErrorConsulta


def main():
    print("=" * 55)
    print("SISTEMA DE CONSULTA - BASE DE DATOS GERIÁTRICA")
    print("=" * 55)

    try:
        resultados = conteos()

        print(f"\n{'TABLA':<35} {'REGISTROS':>12}")
        print("-" * 55)

        total = 0

        for tabla, cantidad in resultados:
            print(f"{tabla:<35} {cantidad:>12}")
            total += cantidad

        print("-" * 55)
        print(f"{'TOTAL DE REGISTROS':<35} {total:>12}")
        print("=" * 55)

    except ErrorConsulta as error:
        print("\n" + str(error))
        print("\nLa operación no pudo completarse.")
        print("=" * 55)


if __name__ == "__main__":
    main()