#!/usr/bin/env python3
"""
Script per la creazione del database MySQL per Movie Catalog.
Questo script crea il database e le tabelle necessarie.
"""

import mysql.connector
from mysql.connector import Error
import json
import os
from pathlib import Path

def load_config():
    """Carica la configurazione dal file di configurazione o richiede all'utente"""
    config_file = Path('mysql_config.json')
    
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Errore nel file di configurazione. Utilizzo dei valori predefiniti.")
    
    # Valori predefiniti
    return {
        'host': 'localhost',
        'user': 'root',
        'password': '22243',
        'database': 'movie_catalog'
    }

def create_database_connection(host, user, password, database=None):
    """Crea una connessione al database MySQL"""
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            auth_plugin='mysql_native_password'
        )
        return connection
    except Error as e:
        print(f"Errore durante la connessione a MySQL: {e}")
        return None

def create_database(cursor, db_name):
    """Crea il database se non esiste"""
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute(f"USE {db_name}")
        print(f"Database '{db_name}' creato con successo o già esistente.")
        return True
    except Error as e:
        print(f"Errore durante la creazione del database: {e}")
        return False

def create_tables(cursor):
    """Crea le tabelle necessarie"""
    try:
        # Tabella movies
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                genre VARCHAR(255),
                movie_name VARCHAR(255),
                title VARCHAR(255),
                year INT,
                path VARCHAR(512) UNIQUE,
                poster_url TEXT,
                backdrop_url TEXT,
                overview TEXT,
                rating FLOAT,
                runtime INT,
                director VARCHAR(255),
                cast_json TEXT,
                genres_json TEXT,
                imdb_id VARCHAR(50),
                last_scanned DATETIME,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        print("Tabelle create con successo.")
        return True
        
    except Error as e:
        print(f"Errore durante la creazione delle tabelle: {e}")
        return False

def main():
    print("=== Configurazione Database Movie Catalog ===\n")
    
    # Carica la configurazione
    config = load_config()
    
    # Connessione al server MySQL (senza selezionare un database specifico)
    connection = create_database_connection(
        config['host'],
        config['user'],
        config['password']
    )
    
    if not connection:
        print("Impossibile connettersi al server MySQL. Verifica le credenziali.")
        return
    
    try:
        cursor = connection.cursor()
        
        # Crea il database
        if not create_database(cursor, config['database']):
            return
        
        # Crea le tabelle
        if not create_tables(cursor):
            return
        
        print("\nConfigurazione del database completata con successo!")
        
    except Error as e:
        print(f"Errore: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connessione a MySQL chiusa.")

if __name__ == "__main__":
    main()
