#!/bin/bash

# Scorre tutte le sottocartelle della directory corrente
for dir in */ ; do
    echo ">>> Entro in $dir"
    cd "$dir" || continue

    # Lancia sbatch su tutti i file .sh (se esistono)
    if ls *.sh 1> /dev/null 2>&1; then
        sbatch *.sh
    else
        echo "Nessun file .sh in $dir"
    fi

    cd ..
done
