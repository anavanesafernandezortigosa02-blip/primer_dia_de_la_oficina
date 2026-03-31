    """Ejercicio de programación lineal / optimización de recursos.

Este script calcula la combinación óptima de unidades (espadachines, arqueros y jinetes)
para maximizar el poder total del ejército dado un stock limitado de comida, madera y oro.

La resolución se hace de manera exacta explorando todas las combinaciones válidas de unidades.
"""

# Datos del problema
recursos = {
    "comida": 1200,
    "madera": 800,
    "oro": 600,
}

unidades = {
    "espadachines": {
        "comida": 60,
        "madera": 20,
        "oro": 0,
        "poder": 70,
    },
    "arqueros": {
        "comida": 80,
        "madera": 10,
        "oro": 40,
        "poder": 95,
    },
    "jinetes": {
        "comida": 140,
        "madera": 0,
        "oro": 100,
        "poder": 230,
    },
}


def calcular_poder(espadachines, arqueros, jinetes):
    return (
        espadachines * unidades["espadachines"]["poder"]
        + arqueros * unidades["arqueros"]["poder"]
        + jinetes * unidades["jinetes"]["poder"]
    )


def recursos_consumidos(espadachines, arqueros, jinetes):
    return {
        "comida": (
            espadachines * unidades["espadachines"]["comida"]
            + arqueros * unidades["arqueros"]["comida"]
            + jinetes * unidades["jinetes"]["comida"]
        ),
        "madera": (
            espadachines * unidades["espadachines"]["madera"]
            + arqueros * unidades["arqueros"]["madera"]
            + jinetes * unidades["jinetes"]["madera"]
        ),
        "oro": (
            espadachines * unidades["espadachines"]["oro"]
            + arqueros * unidades["arqueros"]["oro"]
            + jinetes * unidades["jinetes"]["oro"]
        ),
    }


def es_valida(espadachines, arqueros, jinetes):
    consumos = recursos_consumidos(espadachines, arqueros, jinetes)
    return (
        consumos["comida"] <= recursos["comida"]
        and consumos["madera"] <= recursos["madera"]
        and consumos["oro"] <= recursos["oro"]
    )


def buscar_solucion_optima():
    mejor_poder = 0
    mejor_solucion = None

    # Límites de búsqueda razonables para cada tipo de unidad
    max_espadachines = recursos["comida"] // unidades["espadachines"]["comida"]
    max_arqueros = recursos["comida"] // unidades["arqueros"]["comida"]
    max_jinetes = recursos["comida"] // unidades["jinetes"]["comida"]

    for e in range(max_espadachines + 1):
        for a in range(max_arqueros + 1):
            for j in range(max_jinetes + 1):
                if not es_valida(e, a, j):
                    continue

                poder = calcular_poder(e, a, j)
                if poder > mejor_poder:
                    mejor_poder = poder
                    mejor_solucion = (e, a, j)

    return mejor_solucion, mejor_poder


if __name__ == "__main__":
    solucion, poder_total = buscar_solucion_optima()

    if solucion is None:
        print("No hay ninguna combinación válida de unidades con los recursos dados.")
    else:
        espadachines, arqueros, jinetes = solucion
        consumos = recursos_consumidos(espadachines, arqueros, jinetes)

        print("Solución óptima encontrada:")
        print(f"  Espadachines: {espadachines}")
        print(f"  Arqueros:      {arqueros}")
        print(f"  Jinetes:       {jinetes}")
        print("")
        print("Consumo de recursos:")
        print(f"  Comida: {consumos['comida']} / {recursos['comida']}")
        print(f"  Madera: {consumos['madera']} / {recursos['madera']}")
        print(f"  Oro:    {consumos['oro']} / {recursos['oro']}")
        print("")
        print(f"Poder total máximo: {poder_total}")
