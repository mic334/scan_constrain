#!/bin/sh

# svuota i file prima di scrivere
> energia.dat
> energia_incompleta.dat

# Cicla su tutti i .log e .out
for file in $(find . -type f \( -name "*.log" -o -name "*.out" \)); do
    # Estrai l'ultima riga SCF Done
    last_scf=$(grep "SCF Done" "$file" | tail -n 1)

    # Salta file senza SCF Done
    [ -z "$last_scf" ] && continue

    # Nome della cartella del file
    cartella=$(basename "$(dirname "$file")")

    # Controlla se termina normalmente
    if tail -n 1 "$file" | grep -q "Normal termination"; then
        echo "$cartella : $last_scf" >> energia.dat
    else
        echo "$cartella : $last_scf" >> energia_incompleta.dat
    fi
done