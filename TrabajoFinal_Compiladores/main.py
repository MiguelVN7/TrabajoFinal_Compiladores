import os

def compute_first(productions):
    first = {non_terminal: set() for non_terminal in productions}

    while True:
        updated = False
        for non_terminal in productions:
            for production in productions[non_terminal]:
                if production == 'epsilon':
                    if 'epsilon' not in first[non_terminal]:
                        first[non_terminal].add('epsilon')
                        updated = True
                else:
                    for symbol in production:
                        if symbol in productions:
                            before_update = len(first[non_terminal])
                            first[non_terminal].update(first[symbol] - {'epsilon'})
                            if 'epsilon' not in first[symbol]:
                                break
                        else:
                            if symbol not in first[non_terminal]:
                                first[non_terminal].add(symbol)
                                updated = True
                            break
                    else:
                        if 'epsilon' not in first[non_terminal]:
                            first[non_terminal].add('epsilon')
                            updated = True
        if not updated:
            break

    return first

def compute_follow(productions, first):
    follow = {non_terminal: set() for non_terminal in productions}
    start_symbol = next(iter(productions))
    follow[start_symbol].add('$')

    def first_of_string(string):
        result = set()
        for symbol in string:
            symbol_first = first[symbol] if symbol in productions else {symbol}
            result.update(symbol_first - {'epsilon'})
            if 'epsilon' not in symbol_first:
                break
        else:
            result.add('epsilon')
        return result

    updated = True
    while updated:
        updated = False
        for non_terminal, rules in productions.items():
            for rule in rules:
                follow_temp = follow[non_terminal].copy()
                for i in range(len(rule) - 1, -1, -1):
                    symbol = rule[i]
                    if symbol in productions:
                        before_update = follow[symbol].copy()
                        follow[symbol].update(follow_temp)
                        if follow[symbol] != before_update:
                            updated = True
                        if 'epsilon' in first[symbol]:
                            follow_temp = follow_temp.union(first[symbol] - {'epsilon'})
                        else:
                            follow_temp = first[symbol]
                    else:
                        follow_temp = {symbol}

    return follow

def main():
    input_path = 'C:/Users/Miguel/PycharmProjects/TrabajoFinal_Compiladores/glcs.in'
    output_path = 'C:/Users/Miguel/PycharmProjects/TrabajoFinal_Compiladores/pr_sig.out'

    if not os.path.exists(input_path):
        print(f"Error: El archivo de entrada {input_path} no existe.")
        return

    try:
        with open(input_path, 'r') as infile:
            cases = int(infile.readline().strip())
            print(f"Número de casos: {cases}")
            results = []

            for case_num in range(cases):
                k = int(infile.readline().strip())
                print(f"\nNúmero de no terminales para el caso {case_num + 1}: {k}")
                productions = {}
                for _ in range(k):
                    line = infile.readline().strip()
                    print(f"Producción: {line}")
                    non_terminal, expr = line.split('->')
                    non_terminal = non_terminal.strip()
                    alternatives = [alt.strip() for alt in expr.split('|')]
                    productions[non_terminal] = alternatives

                print(f"Producciones para el caso {case_num + 1}: {productions}")
                first = compute_first(productions)
                print(f"Conjuntos Primero para el caso {case_num + 1}: {first}")
                follow = compute_follow(productions, first)
                print(f"Conjuntos Siguiente para el caso {case_num + 1}: {follow}")

                result = []
                result.append(f"{k}")
                for non_terminal in productions:
                    first_set = ', '.join(sorted(first[non_terminal]))
                    result.append(f"Pr({non_terminal}) = {{{first_set}}}")
                for non_terminal in productions:
                    follow_set = ', '.join(sorted(follow[non_terminal]))
                    result.append(f"Sig({non_terminal}) = {{{follow_set}}}")
                results.append(result)

        with open(output_path, 'w') as outfile:
            outfile.write(f"{cases}\n")
            for result in results:
                outfile.write('\n'.join(result) + '\n')

        print(f"\nEl archivo de salida se ha generado correctamente en {output_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
