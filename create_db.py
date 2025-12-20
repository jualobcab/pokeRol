#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear la base de datos PokéRol desde el archivo SQL
"""

import sqlite3
import os

def create_database():
    """Crea la base de datos desde el archivo SQL"""
    db_path = 'pokeRol.db'
    sql_path = 'database/pokeRol.sql'
    
    # Leer el archivo SQL
    try:
        with open(sql_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
    except UnicodeDecodeError:
        with open(sql_path, 'r', encoding='latin-1') as f:
            sql_content = f.read()
    
    # Crear la base de datos
    conn = sqlite3.connect(db_path)
    conn.executescript(sql_content)
    conn.close()
    
    print(f"✅ Base de datos creada exitosamente en: {db_path}")

if __name__ == '__main__':
    create_database()