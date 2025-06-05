def distance(s1: str, s2: str) -> int:
    """
    Calcula la distancia de Levenshtein entre dos strings.
    Esta es una implementación simple y eficiente.
    
    Args:
        s1: Primer string
        s2: Segundo string
        
    Returns:
        Distancia de Levenshtein entre s1 y s2
    """
    if len(s1) < len(s2):
        return distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def hamming_distance(s1: str, s2: str) -> int:
    """
    Calcula la distancia de Hamming entre dos strings de igual longitud.
    La distancia de Hamming es el número de posiciones en las que 
    los caracteres correspondientes son diferentes.
    
    Args:
        s1: Primer string
        s2: Segundo string
        
    Returns:
        Distancia de Hamming entre s1 y s2
        
    Raises:
        ValueError: Si los strings tienen longitudes diferentes
    """
    if len(s1) != len(s2):
        raise ValueError("Los strings deben tener la misma longitud para calcular la distancia de Hamming")
    
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def hamming_distance_with_padding(s1: str, s2: str, pad_char: str = ' ') -> int:
    """
    Calcula la distancia de Hamming entre dos strings de diferentes longitudes,
    rellenando el string más corto con un carácter específico.
    
    Args:
        s1: Primer string
        s2: Segundo string
        pad_char: Carácter para rellenar (por defecto, espacio)
        
    Returns:
        Distancia de Hamming con padding
    """
    if len(pad_char) != 1:
        raise ValueError("El carácter de relleno debe ser exactamente un carácter")
    
    max_len = max(len(s1), len(s2))
    s1_padded = s1.ljust(max_len, pad_char)
    s2_padded = s2.ljust(max_len, pad_char)
    
    return sum(c1 != c2 for c1, c2 in zip(s1_padded, s2_padded)) 