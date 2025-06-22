import mysql.connector
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import csv
import logging
import urllib.parse
import re
import time

# Create a logger
logger = logging.getLogger(__name__)

class MySQLConfig:
    def __init__(self, root=None):
        self.root = root
        self.config_file = 'mysql_config.json'
        self.default_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '22243',
            'database': 'movie_catalog'
        }
        self.config = self.load_config()
        
    def show_config_form(self):
        if not self.root:
            return self.config
            
        def save_and_close():
            config = {
                'host': host_entry.get(),
                'user': user_entry.get(),
                'password': password_entry.get(),
                'database': database_entry.get()
            }
            if self.save_config(config):
                messagebox.showinfo("Success", "Configuration saved successfully!")
                config_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to save configuration")
                
        config_window = tk.Toplevel(self.root)
        
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return self.default_config
        return self.default_config
        
    def save_config(self, config):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
            
    def show_config_form(self):
        def save_and_close():
            config = {
                'host': host_entry.get(),
                'user': user_entry.get(),
                'password': password_entry.get(),
                'database': database_entry.get()
            }
            if self.save_config(config):
                messagebox.showinfo("Success", "Configuration saved successfully!")
                config_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to save configuration")
                
        config_window = tk.Toplevel()
        config_window.title("MySQL Configuration")
        config_window.geometry("400x400")
        
        # Create form elements
        ttk.Label(config_window, text="Host:").pack(pady=5)
        host_entry = ttk.Entry(config_window)
        host_entry.pack(pady=5)
        host_entry.insert(0, self.config['host'])
        
        ttk.Label(config_window, text="Username:").pack(pady=5)
        user_entry = ttk.Entry(config_window)
        user_entry.pack(pady=5)
        user_entry.insert(0, self.config['user'])
        
        ttk.Label(config_window, text="Password:").pack(pady=5)
        password_entry = ttk.Entry(config_window, show="*")
        password_entry.pack(pady=5)
        password_entry.insert(0, self.config['password'])
        
        ttk.Label(config_window, text="Database Name:").pack(pady=5)
        database_entry = ttk.Entry(config_window)
        database_entry.pack(pady=5)
        database_entry.insert(0, self.config['database'])
        
        # Save button
        save_button = ttk.Button(config_window, text="Save Configuration", command=save_and_close)
        save_button.pack(pady=20)

class MySQLDatabase:
    def __init__(self, root):
        self.config = MySQLConfig(root)
        # Configura il logger
        self.logger = logging.getLogger('struttura.logger.Database')
        
        # Show config form and wait for it to complete
        self.root = root
        self.root.withdraw()  # Hide the root window
        self.config.show_config_form()
        self.root.deiconify()  # Show the root window again
        
        self.host = self.config.config['host']
        self.user = self.config.config['user']
        self.password = self.config.config['password']
        self.database = self.config.config['database']
        self.connection = None
        self.cursor = None
        self.is_mysql = True
        self.logger.info(f"Database config: host={self.host}, database={self.database}")

    def create_connection(self):
        """Create and return a new database connection"""
        if not all([self.host, self.user, self.password, self.database]):
            self.logger.error("Parametri di connessione al database mancanti o non validi")
            return None
            
        config = {
            'host': self.host,
            'user': self.user,
            'password': self.password,
            'database': self.database,
            'auth_plugin': 'mysql_native_password',
            'connection_timeout': 10,  # Aumentato il timeout a 10 secondi
            'connect_timeout': 10,     # Timeout per la connessione iniziale
            'pool_name': 'movie_catalog_pool',
            'pool_size': 5
        }
        
        try:
            self.logger.info(f"Attempting to connect to MySQL at {self.host}...")
            self.connection = mysql.connector.connect(**config)
            
            # Imposta il timeout delle operazioni a 300 secondi (5 minuti)
            self.connection.timeout = 300
            
            self.logger.info("MySQL connection successful")
            return self.connection
            
        except mysql.connector.Error as err:
            error_msg = f"""
            Cannot connect to MySQL server.
            Error: {err}
            
            Please verify that:
            1. MySQL server is installed and running
            2. The connection details are correct:
               - Host: {self.host}
               - User: {self.user}
               - Database: {self.database}
            3. The MySQL service is running
            4. The port (default 3306) is not blocked by firewall
            5. The user has proper permissions
            """
            self.logger.error(error_msg)
            messagebox.showerror("MySQL Connection Error", error_msg)
            return None
            
    def create_database(self):
        """Create the database if it doesn't exist"""
        conn = None
        try:
            print(f"Creating database {self.database} if it doesn't exist...")
            # First connect without database parameter
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                auth_plugin='mysql_native_password',
                connection_timeout=5
            )
            cursor = conn.cursor()
            
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.execute(f"USE {self.database}")
            
            # Store the connection
            self.connection = conn
            self.cursor = cursor
            
            print(f"Database {self.database} is ready")
            return conn
            
        except mysql.connector.Error as err:
            error_msg = f"Error creating database: {err}"
            print(error_msg)
            messagebox.showerror("MySQL Error", error_msg)
            if conn and conn.is_connected():
                conn.close()
            return None
            
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        if not self.connection or not self.connection.is_connected():
            if not self.create_connection():
                return False
                
        cursor = self.connection.cursor(dictionary=True)
        try:
            # Create movies table with all necessary columns
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
            
            # Add any missing columns
            cursor.execute("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'movies'
            """, (self.database,))
            
            existing_columns = [col['COLUMN_NAME'] for col in cursor.fetchall()]
            
            # Add missing columns if they don't exist
            columns_to_add = [
                ("genre", "ALTER TABLE movies ADD COLUMN genre VARCHAR(255) AFTER id"),
                ("movie_name", "ALTER TABLE movies ADD COLUMN movie_name VARCHAR(255) AFTER genre"),
                ("title", "ALTER TABLE movies ADD COLUMN title VARCHAR(255) AFTER movie_name"),
                ("year", "ALTER TABLE movies ADD COLUMN year INT AFTER title"),
                ("poster_url", "ALTER TABLE movies ADD COLUMN poster_url TEXT AFTER path"),
                ("backdrop_url", "ALTER TABLE movies ADD COLUMN backdrop_url TEXT AFTER poster_url"),
                ("overview", "ALTER TABLE movies ADD COLUMN overview TEXT AFTER backdrop_url"),
                ("rating", "ALTER TABLE movies ADD COLUMN rating FLOAT AFTER overview"),
                ("runtime", "ALTER TABLE movies ADD COLUMN runtime INT AFTER rating"),
                ("director", "ALTER TABLE movies ADD COLUMN director VARCHAR(255) AFTER runtime"),
                ("cast_json", "ALTER TABLE movies ADD COLUMN cast_json TEXT AFTER director"),
                ("genres_json", "ALTER TABLE movies ADD COLUMN genres_json TEXT AFTER cast_json"),
                ("imdb_id", "ALTER TABLE movies ADD COLUMN imdb_id VARCHAR(50) AFTER genres_json"),
                ("last_scanned", "ALTER TABLE movies ADD COLUMN last_scanned DATETIME AFTER imdb_id"),
                ("created_at", "ALTER TABLE movies ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP AFTER last_scanned"),
                ("updated_at", "ALTER TABLE movies ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP AFTER created_at")
            ]
            
            for column_name, alter_query in columns_to_add:
                if column_name not in existing_columns:
                    try:
                        cursor.execute(alter_query)
                        print(f"Added column: {column_name}")
                    except mysql.connector.Error as err:
                        print(f"Error adding column {column_name}: {err}")
            
            self.connection.commit()
            return True
            
        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error creating/updating tables: {err}")
            return False
            
    def close(self):
        """Close the database connection"""
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None

    def add_movie(self, genre, movie_name, path):
        conn = self.create_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO movies (genre, movie_name, path, last_scanned)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                genre = VALUES(genre),
                movie_name = VALUES(movie_name),
                last_scanned = VALUES(last_scanned)
            ''', (genre, movie_name, path, datetime.now()))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error adding movie: {err}")
            return False
        finally:
            cursor.close()
            conn.close()
            
    def get_all_movies(self, sort_by='title', sort_order='ASC'):
        """Restituisce tutti i film dal database con ordinamento personalizzato"""
        try:
            # Mappa i nomi dei campi alle colonne del database
            field_map = {
                'id': 'id',
                'title': 'title',
                'year': 'year',
                'genre': 'genre',
                'rating': 'rating',
                'runtime': 'runtime',
                'path': 'path',
                'movie_name': 'movie_name'
            }
            
            # Imposta il campo di ordinamento predefinito se non valido
            sort_field = field_map.get(sort_by, 'title')
            
            # Assicurati che l'ordine sia valido
            sort_order = sort_order.upper()
            if sort_order not in ('ASC', 'DESC'):
                sort_order = 'ASC'
            
            # Costruisci la query con ordinamento dinamico
            query = f"""
                SELECT * FROM movies 
                ORDER BY {sort_field} {sort_order}, 
                         title {sort_order}
            """
            
            self.cursor.execute(query)
            return self.cursor.fetchall()
            
        except Exception as e:
            self.logger.error(f"Errore nel recupero dei film: {str(e)}")
            raise
            
    def store_scanned_files(self, files):
        """
        Store a list of scanned files in the database.
        
        Args:
            files: List of tuples containing (genre, movie_name, path)
        
        Returns:
            bool: True if all files were stored successfully, False otherwise
        """
        conn = self.create_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()
        try:
            # Prepare the SQL statement
            sql = '''
                INSERT INTO movies (genre, movie_name, path, last_scanned)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                genre = VALUES(genre),
                movie_name = VALUES(movie_name),
                last_scanned = VALUES(last_scanned)
            '''
            
            # Add timestamp to each file tuple
            files_with_timestamp = [(genre, movie_name, path, datetime.now()) 
                                  for genre, movie_name, path in files]
            
            # Execute the query with multiple rows
            cursor.executemany(sql, files_with_timestamp)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error storing files: {err}")
            return False
        finally:
            cursor.close()
            conn.close()
            
    def export_to_csv(self, filename):
        """
        Esporta tutti i film in un file CSV con codifica UTF-8 BOM
        
        Args:
            filename: Percorso del file CSV di destinazione
            
        Returns:
            bool: True se l'esportazione è riuscita, False altrimenti
        """
        try:
            # Recupera tutti i film dal database
            movies = self.get_all_movies()
            
            if not movies:
                self.logger.warning("Nessun film da esportare")
                return False
                
            # Ottieni i nomi delle colonne dal primo film
            columns = [desc[0] for desc in self.cursor.description]
            
            # Aggiungi BOM (Byte Order Mark) per UTF-8
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=columns, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                
                # Scrivi l'header con i nomi delle colonne
                writer.writeheader()
                
                # Scrivi i dati dei film
                for movie in movies:
                    writer.writerow(dict(zip(columns, movie)))
            
            self.logger.info(f"Esportati {len(movies)} film in {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Errore durante l'esportazione in CSV: {str(e)}")
            return False

    def import_from_csv(self, file_path, skip_duplicates=True, update_existing=False):
        """
        Importa film da un file CSV con codifica UTF-8 BOM.
        
        Args:
            file_path: Percorso del file CSV da importare
            skip_duplicates: Se True, salta i duplicati invece di aggiornarli
            update_existing: Se True, aggiorna i film esistenti invece di saltarli
            
        Returns:
            tuple: (imported_count, skipped_count, error_count, error_details)
        """
        if not os.path.exists(file_path):
            self.logger.error(f"File non trovato: {file_path}")
            return 0, 0, 1, [f"File non trovato: {file_path}"]
            
        imported_count = 0
        skipped_count = 0
        error_count = 0
        error_details = []
        
        try:
            # Prova a rilevare la codifica del file
            with open(file_path, 'rb') as f:
                raw = f.read(4)
                # Se inizia con BOM, usa utf-8-sig, altrimenti prova utf-8
                encoding = 'utf-8-sig' if raw.startswith(b'\xef\xbb\xbf') else 'utf-8'
            
            # Leggi il file CSV con la codifica rilevata
            with open(file_path, 'r', encoding=encoding, newline='', errors='replace') as csvfile:
                # Prova a rilevare il delimitatore
                try:
                    dialect = csv.Sniffer().sniff(csvfile.read(1024))
                    csvfile.seek(0)
                except:
                    # Usa le impostazioni predefinite se il rilevamento fallisce
                    dialect = 'excel'
                
                # Leggi il file CSV
                reader = csv.DictReader(csvfile, dialect=dialect)
                
                # Verifica i campi obbligatori
                required_fields = {'title', 'path'}
                missing_fields = required_fields - set(reader.fieldnames or [])
                if missing_fields:
                    error_msg = f"Campi obbligatori mancanti: {', '.join(missing_fields)}"
                    self.logger.error(error_msg)
                    return 0, 0, 1, [error_msg]
                
                # Elabora ogni riga del CSV
                for row_num, row in enumerate(reader, 2):  # Inizia da 2 per la numerazione delle righe (1-based + header)
                    try:
                        # Pulisci i valori
                        row = {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
                        
                        # Verifica i campi obbligatori
                        if not row.get('title') or not row.get('path'):
                            error_msg = f"Riga {row_num}: Campi obbligatori mancanti (titolo o percorso)"
                            error_details.append(error_msg)
                            error_count += 1
                            continue
                        
                        # Verifica se il film esiste già
                        existing = self.get_movie_by_path(row['path'])
                        
                        if existing and skip_duplicates and not update_existing:
                            # Salta i duplicati
                            skipped_count += 1
                            continue
                        
                        # Prepara i dati per l'inserimento/aggiornamento
                        movie_data = {
                            'genre': row.get('genre', ''),
                            'movie_name': row.get('movie_name', ''),
                            'title': row['title'],
                            'year': int(row['year']) if row.get('year') and row['year'].isdigit() else None,
                            'path': row['path'],
                            'poster_url': row.get('poster_url', ''),
                            'backdrop_url': row.get('backdrop_url', ''),
                            'overview': row.get('overview', ''),
                            'rating': float(row['rating']) if row.get('rating') and row['rating'].replace('.', '', 1).isdigit() else None,
                            'runtime': int(row['runtime']) if row.get('runtime') and row['runtime'].isdigit() else None,
                            'director': row.get('director', ''),
                            'imdb_id': row.get('imdb_id', ''),
                            'cast_json': row.get('cast_json', '[]'),
                            'genres_json': row.get('genres_json', '[]')
                        }
                        
                        if existing and update_existing:
                            # Aggiorna il film esistente
                            self.update_movie(existing[0], **movie_data)
                        else:
                            # Inserisci un nuovo film
                            self.add_movie(**movie_data)
                        
                        imported_count += 1
                        
                    except Exception as e:
                        error_msg = f"Riga {row_num}: Errore durante l'importazione - {str(e)}"
                        error_details.append(error_msg)
                        error_count += 1
                        self.logger.error(f"Errore durante l'importazione della riga {row_num}: {str(e)}")
            
            return imported_count, skipped_count, error_count, error_details
            
        except Exception as e:
            error_msg = f"Errore durante l'importazione del file CSV: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return imported_count, skipped_count, error_count + 1, error_details + [error_msg]

    def clean_value(self, value):
        """
        Clean a single value by removing URL-encoded sequences and normalizing
        Handles various URL-encoded patterns and special characters
        """
        if value is None:
            return None
            
        if not isinstance(value, str):
            try:
                value = str(value)
            except:
                return value
        
        # Common URL-encoded sequences to replace
        replacements = {
            # Standard URL-encoded sequences
            '+AFs-': '[',    # URL-encoded '['
            '+AF0-': ']',    # URL-encoded ']'
            '+AFw-': '\\\\', # URL-encoded '\\' (escaped for Python string)
            '+AF8-': '_',    # URL-encoded '_'
            '+AC0-': '-',    # URL-encoded '-'
            '+ACE-': '!',    # URL-encoded '!'
            '+ACU-': '%',    # URL-encoded '%'
            '+ACU24': '$',   # URL-encoded '$'
            '+ACU26': '&',   # URL-encoded '&'
            '+ACU2B': '+',   # URL-encoded '+'
            '+ACU2C': ',',   # URL-encoded ','
            '+ACU2F': '/',   # URL-encoded '/'
            '+ACU3A': ':',   # URL-encoded ':'
            '+ACU3B': ';',   # URL-encoded ';'
            '+ACU3D': '=',   # URL-encoded '='
            '+ACU3F': '?',   # URL-encoded '?'
            '+ACU40': '@',   # URL-encoded '@'
            '+ACU5B': '[',   # URL-encoded '['
            '+ACU5D': ']',   # URL-encoded ']'
            '+ACU5E': '^',   # URL-encoded '^'
            '+ACU60': '`',   # URL-encoded '`'
            '+ACU7B': '{',   # URL-encoded '{'
            '+ACU7C': '|',   # URL-encoded '|'
            '+ACU7D': '}',   # URL-encoded '}'
            '+ACU7E': '~',   # URL-encoded '~'
            '+ACU22': '"',  # URL-encoded '"'
            '+ACU27': "'",  # URL-encoded "'"
            '+ACU3C': '<',   # URL-encoded '<'
            '+ACU3E': '>',   # URL-encoded '>'
            '+ACU23': '#',   # URL-encoded '#'
            '+ACU25': '%',   # URL-encoded '%'
            
            # Italian accented characters (URL-encoded)
            '+//3//Q-': 'à',
            '+//3//U-': 'è',
            '+//3//Y-': 'ì',
            '+//3//c-': 'ò',
            '+//3//w-': 'ù',
            '+//3//0-': 'À',
            '+//3//4-': 'È',
            '+//3//8-': 'Ì',
            '+//3//A-': 'Ò',
            '+//3//M-': 'Ù',
            
            # Common HTML entities that might appear
            '&agrave;': 'à',
            '&egrave;': 'è',
            '&igrave;': 'ì',
            '&ograve;': 'ò',
            '&ugrave;': 'ù',
            '&Agrave;': 'À',
            '&Egrave;': 'È',
            '&Igrave;': 'Ì',
            '&Ograve;': 'Ò',
            '&Ugrave;': 'Ù',
            '&eacute;': 'é',
            '&Eacute;': 'É',
            '&egrave;': 'è',
            '&Egrave;': 'È',
            '&agrave;': 'à',
            '&Agrave;': 'À',
            '&igrave;': 'ì',
            '&Igrave;': 'Ì',
            '&ograve;': 'ò',
            '&Ograve;': 'Ò',
            '&ugrave;': 'ù',
            '&Ugrave;': 'Ù',
            '&quot;': '"',
            '&amp;': '&',
            '&lt;': '<',
            '&gt;': '>',
            '&apos;': "'"
        }
        
        # First, replace known URL-encoded sequences
        cleaned = value
        for seq, replacement in replacements.items():
            cleaned = cleaned.replace(seq, replacement)
        
        # Try to decode any remaining URL-encoded sequences
        import urllib.parse
        import html
        
        try:
            # Try to decode as UTF-8 first
            cleaned = urllib.parse.unquote(cleaned)
            # Decode HTML entities
            cleaned = html.unescape(cleaned)
        except Exception as e:
            print(f"Error decoding value: {e}")
            pass
            
        # Clean up any remaining special characters
        import re
        # Allow common punctuation and accented characters
        cleaned = re.sub(r'[^\x20-\x7E\n\r\t\u00C0-\u00FF]', '', cleaned)
        
        # Clean up any double spaces that might have been created
        cleaned = ' '.join(cleaned.split())
        
        return cleaned.strip()

    def decode_path(encoded_path):
        """
        Decodifica un percorso che potrebbe essere stato codificato più volte.
        Gestisce i casi di doppia codifica e caratteri speciali.
        """
        if not encoded_path:
            return ""
        
        try:
            # Se il percorso contiene sequenze di codifica URL, prova a decodificarle
            if any(seq in encoded_path for seq in ['%', '+AF8AXA-', '+AFwAXA-']):
                # Sostituisci le sequenze problematiche
                decoded = encoded_path
                
                # Gestisci le sequenze di codifica comuni
                replacements = {
                    '+AF8AXA-': '\\',  # Sostituisce la sequenza codificata per \\
                    '+AFwAXA-': '\\',  # Altra variante
                    '+AF8-': '_',       # Sostituisce la sequenza codificata per _
                    '+AC0-': '-',       # Sostituisce la sequenza codificata per -
                    '+ACo-': '~',       # Sostituisce la sequenza codificata per ~
                    '+ADw-': '<',       # Sostituisce la sequenza codificata per <
                    '+AD4-': '>',       # Sostituisce la sequenza codificata per >
                    '+ADs-': ';',       # Sostituisce la sequenza codificata per ;
                    '+ACs-': '+',       # Sostituisce la sequenza codificata per +
                    '+AD0-': '=',       # Sostituisce la sequenza codificata per =
                    '+AC0-': '&',       # Sostituisce la sequenza codificata per &
                    '+ADw-': '(',       # Sostituisce la sequenza codificata per (
                    '+AD4-': ')'        # Sostituisce la sequenza codificata per )
                }
                
                # Applica le sostituzioni
                for seq, replacement in replacements.items():
                    decoded = decoded.replace(seq, replacement)
                
                # Prova a decodificare eventuali sequenze URL-encoded
                try:
                    decoded = urllib.parse.unquote(decoded)
                except:
                    pass
                
                # Normalizza i separatori di percorso
                decoded = decoded.replace('\\', '/')
                
                # Rimuovi eventuali doppi separatori
                decoded = re.sub(r'/+', '/', decoded)
                
                return decoded
                
            return encoded_path
            
        except Exception as e:
            print(f"Errore nella decodifica del percorso {encoded_path}: {e}")
            return encoded_path

    def get_movie_by_id(self, movie_id):
        """
        Get a movie by its ID
        
        Args:
            movie_id: ID of the movie to retrieve
            
        Returns:
            dict: Movie details or None if not found
        """
        conn = self.create_connection()
        if not conn:
            return None
            
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('''
                SELECT id, genre, movie_name, title, year, path, 
                       poster_url, backdrop_url, overview, rating,
                       director, actors, imdb_id, last_scanned
                FROM movies 
                WHERE id = %s
            ''', (movie_id,))
            
            movie = cursor.fetchone()
            
            # Decodifica il percorso se presente
            if movie and 'path' in movie and movie['path']:
                movie['path'] = self.decode_path(movie['path'])
                
            return movie
            
        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error fetching movie: {err}")
            return None
        finally:
            cursor.close()
            conn.close()
            
    def empty_database(self):
        """Svuota la tabella movies del database"""
        conn = None
        cursor = None
        max_retries = 3
        retry_delay = 2  # secondi
        
        for attempt in range(max_retries):
            try:
                conn = self.create_connection()
                if not conn:
                    self.logger.error("Impossibile stabilire una connessione al database")
                    return False
                    
                cursor = conn.cursor()
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                cursor.execute("TRUNCATE TABLE movies")
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
                conn.commit()
                self.logger.info("Tabella 'movies' svuotata con successo")
                return True
                
            except mysql.connector.Error as err:
                error_msg = f"Errore MySQL durante lo svuotamento (tentativo {attempt + 1}/{max_retries}): {str(err)}"
                self.logger.error(error_msg)
                
                if "Lost connection" in str(err) and attempt < max_retries - 1:
                    self.logger.info(f"Tentativo di riconnessione in corso... ({attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    try:
                        if conn and conn.is_connected():
                            conn.reconnect(attempts=3, delay=retry_delay)
                    except Exception as reconnect_err:
                        self.logger.error(f"Errore durante la riconnessione: {str(reconnect_err)}")
                    continue
                    
                messagebox.showerror("Errore Database", f"Impossibile svuotare il database: {str(err)}")
                return False
                
            except Exception as e:
                error_msg = f"Errore imprevisto durante lo svuotamento: {str(e)}"
                self.logger.error(error_msg, exc_info=True)
                messagebox.showerror("Errore", error_msg)
                return False
                
            finally:
                if cursor:
                    cursor.close()
                if conn and conn.is_connected():
                    conn.close()
