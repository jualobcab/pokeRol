#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicación web PokéRol - Creador de Pokémons
Aplicación Flask para crear y gestionar pokémons en la base de datos PokéRol
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os
from contextlib import contextmanager

# Configuración de la aplicación
app = Flask(__name__)
app.secret_key = 'pokemon_secret_key_2025'  # Cambia esto por algo más seguro en producción

# Ruta a la base de datos
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pokeRol.db')

@contextmanager
def get_db_connection():
    """Context manager para manejar conexiones a la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_database():
    """Verifica que la base de datos tenga las tablas necesarias con datos"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Verificar que las tablas principales tengan datos
        tables_to_check = ['sizes', 'types', 'abilities', 'environments', 'habitats', 'proficiencies', 'senses']
        
        for table in tables_to_check:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                if count == 0:
                    print(f"⚠️ Advertencia: La tabla '{table}' está vacía")
                else:
                    print(f"✅ Tabla '{table}': {count} registros")
            except sqlite3.Error as e:
                print(f"❌ Error verificando tabla '{table}': {e}")
        
        conn.commit()

def get_reference_data():
    """Obtiene los datos de referencia necesarios para el formulario"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Obtener tamaños
        cursor.execute("SELECT id, name FROM sizes ORDER BY id")
        sizes = cursor.fetchall()
        
        # Obtener tipos
        cursor.execute("SELECT id, name FROM types ORDER BY name")
        types = cursor.fetchall()
        
        # Obtener habilidades
        cursor.execute("SELECT id, name, legendary FROM abilities ORDER BY name")
        abilities = cursor.fetchall()
        
        # Obtener entornos/ambientes
        cursor.execute("SELECT id, name FROM environments ORDER BY name")
        environments = cursor.fetchall()
        
        # Obtener hábitats
        cursor.execute("SELECT id, name FROM habitats ORDER BY name")
        habitats = cursor.fetchall()
        
        # Obtener proficiencias
        cursor.execute("SELECT id, name FROM proficiencies ORDER BY name")
        proficiencies = cursor.fetchall()
        
        # Obtener sentidos
        cursor.execute("SELECT id, name FROM senses ORDER BY name")
        senses = cursor.fetchall()
        
        return {
            'sizes': sizes,
            'types': types,
            'abilities': abilities,
            'environments': environments,
            'habitats': habitats,
            'proficiencies': proficiencies,
            'senses': senses
        }

def create_pokemon(form_data):
    """Crea un nuevo pokémon en la base de datos"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Manejar intercalado de pokémons
            dex_num = int(form_data['dex_num'])
            intercalar = form_data.get('intercalar_pokemon', False)
            updated_count = 0  # Inicializar contador
            
            if intercalar:
                print(f"🔄 Intercalando pokémon en posición {dex_num}")
                # Incrementar en +1 todos los pokémons con dex_num >= al nuevo número
                cursor.execute("""
                    UPDATE pokemons 
                    SET dex_num = dex_num + 1 
                    WHERE dex_num >= ?
                """, (dex_num,))
                
                updated_count = cursor.rowcount
                print(f"✅ {updated_count} pokémons desplazados +1 desde la posición {dex_num}")
            
            # Los números de pokédex pueden repetirse (diferentes formas, mega evoluciones, etc.)
            # No validamos duplicados
            
            # Validaciones adicionales
            types = form_data.get('types', [])
            if not types:
                return False, "Debes seleccionar al menos un tipo"
            if len(types) > 2:
                return False, "No puedes seleccionar más de 2 tipos"
            
            # Obtener listas de habilidades y proficiencias
            abilities = form_data.get('abilities', [])
            hidden_abilities = form_data.get('hidden_abilities', [])
            proficiencies = form_data.get('proficiencies', [])
            
            # Validar límites de habilidades y proficiencias
            if len(abilities) > 3:
                return False, "No puedes seleccionar más de 3 habilidades"
            
            if len(hidden_abilities) > 2:
                return False, "No puedes seleccionar más de 2 habilidades ocultas"
            
            if len(proficiencies) > 2:
                return False, "No puedes seleccionar más de 2 proficiencias"
            
            # Validar nivel mínimo
            min_level = int(form_data.get('min_level', 1))
            if min_level < 1 or min_level > 20:
                return False, "El nivel mínimo debe estar entre 1 y 20"
            
            # Validar sexo
            valid_sexes = ['', 'M', 'H', 'M/H', '???']
            if form_data.get('sex', '') not in valid_sexes:
                return False, "Sexo no válido"
            
            # Combinar estadísticas con estrellas
            def combine_stat(num_key, star_key):
                num = form_data.get(num_key, '')
                star = form_data.get(star_key, '')
                if not num:
                    return ''
                return str(num) + star
            
            evasion = combine_stat('evasion_num', 'evasion_star')
            vitality = combine_stat('vitality_num', 'vitality_star')
            strength = combine_stat('strength_num', 'strength_star')
            agility = combine_stat('agility_num', 'agility_star')
            endurance = combine_stat('endurance_num', 'endurance_star')
            mind = combine_stat('mind_num', 'mind_star')
            spirit = combine_stat('spirit_num', 'spirit_star')
            presence = combine_stat('presence_num', 'presence_star')
            
            # Validar que todas las estadísticas estén presentes
            if not all([evasion, vitality, strength, agility, endurance, mind, spirit, presence]):
                return False, "Todas las estadísticas son requeridas"
            
            # Validar campos obligatorios básicos
            if not form_data.get('diet', '').strip():
                return False, "La dieta es obligatoria"
            
            if not form_data.get('sex', ''):
                return False, "El sexo es obligatorio"
            
            # Validar que al menos una habilidad normal esté seleccionada
            if not abilities:
                return False, "Debes seleccionar al menos 1 habilidad"
            
            # Validar que al menos una habilidad oculta esté seleccionada
            if not hidden_abilities:
                return False, "Debes seleccionar al menos 1 habilidad oculta"
            
            # Validar que al menos un hábitat esté seleccionado
            habitats = form_data.get('habitats', [])
            if not habitats:
                return False, "Debes seleccionar al menos 1 hábitat"
            
            # Validar que al menos una proficiencia esté seleccionada
            if not proficiencies:
                return False, "Debes seleccionar al menos 1 proficiencia"
            
            # Validar que la velocidad Normal esté seleccionada
            environments = form_data.get('environments', [])
            normal_env_selected = False
            
            # Buscar el ID del entorno "Normal"
            cursor.execute("SELECT id FROM environments WHERE name = 'Normal'")
            normal_env_result = cursor.fetchone()
            if normal_env_result:
                normal_env_id = str(normal_env_result[0])
                if normal_env_id in environments:
                    normal_env_selected = True
            
            if not normal_env_selected:
                return False, "Debe seleccionar la velocidad Normal"
            
            # Insertar el pokémon principal
            pokemon_data = (
                dex_num,  # Usar la variable local en lugar de form_data['dex_num']
                form_data['name'],
                form_data['size_id'],
                evasion,
                vitality,
                strength,
                agility,
                endurance,
                mind,
                spirit,
                presence,
                form_data['min_level'],
                form_data['capture_rate'],
                form_data.get('diet', ''),
                form_data.get('sex', ''),
                0,  # sex_differences
                0,  # different_forms
                form_data.get('description', '')
            )
            
            cursor.execute("""
                INSERT INTO pokemons (
                    dex_num, name, size_id, evasion, vitality, strength, 
                    agility, endurance, mind, spirit, presence, min_level, 
                    capture_rate, diet, sex, sex_differences, different_forms, description
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, pokemon_data)
            
            pokemon_id = cursor.lastrowid
            
            # Limpiar registros previos por si hay datos corruptos de intentos anteriores
            cursor.execute("DELETE FROM pokemon_types WHERE pokemon_id = ?", (pokemon_id,))
            cursor.execute("DELETE FROM pokemon_abilities WHERE pokemon_id = ?", (pokemon_id,))
            cursor.execute("DELETE FROM pokemon_hidden_abilities WHERE pokemon_id = ?", (pokemon_id,))
            cursor.execute("DELETE FROM pokemon_habitats WHERE pokemon_id = ?", (pokemon_id,))
            cursor.execute("DELETE FROM pokemon_proficiencies WHERE pokemon_id = ?", (pokemon_id,))
            cursor.execute("DELETE FROM pokemon_senses WHERE pokemon_id = ?", (pokemon_id,))
            cursor.execute("DELETE FROM pokemon_velocities WHERE pokemon_id = ?", (pokemon_id,))
            
            # Insertar tipos (validación ya realizada arriba)
            # Eliminar duplicados manteniendo el orden
            unique_types = []
            for type_id in types:
                if type_id not in unique_types:
                    unique_types.append(type_id)
            
            for type_id in unique_types:
                cursor.execute(
                    "INSERT INTO pokemon_types (pokemon_id, type_id) VALUES (?, ?)",
                    (pokemon_id, type_id)
                )
            
            # Insertar habilidades si las hay
            abilities = form_data.get('abilities', [])
            for ability_id in abilities:
                cursor.execute(
                    "INSERT INTO pokemon_abilities (pokemon_id, ability_id) VALUES (?, ?)",
                    (pokemon_id, ability_id)
                )
            
            # Insertar habilidades ocultas si las hay
            hidden_abilities = form_data.get('hidden_abilities', [])
            for ability_id in hidden_abilities:
                cursor.execute(
                    "INSERT INTO pokemon_hidden_abilities (pokemon_id, ability_id) VALUES (?, ?)",
                    (pokemon_id, ability_id)
                )
            
            # Insertar hábitats si los hay
            habitats = form_data.get('habitats', [])
            for habitat_id in habitats:
                cursor.execute(
                    "INSERT INTO pokemon_habitats (pokemon_id, habitat_id) VALUES (?, ?)",
                    (pokemon_id, habitat_id)
                )
            
            # Insertar proficiencias si las hay
            proficiencies = form_data.get('proficiencies', [])
            for prof_id in proficiencies:
                cursor.execute(
                    "INSERT INTO pokemon_proficiencies (pokemon_id, proficiency_id) VALUES (?, ?)",
                    (pokemon_id, prof_id)
                )
            
            # Insertar sentidos si los hay
            senses = form_data.get('senses', [])
            for sense_id in senses:
                sense_quantity = form_data.get(f'sense_quantity_{sense_id}', '')
                cursor.execute(
                    "INSERT INTO pokemon_senses (pokemon_id, sense_id, quantity) VALUES (?, ?, ?)",
                    (pokemon_id, sense_id, sense_quantity)
                )
            
            # Insertar velocidades por entorno si las hay
            environments = form_data.get('environments', [])
            for env_id in environments:
                env_quantity = form_data.get(f'env_quantity_{env_id}', 0)
                if env_quantity and int(env_quantity) > 0:
                    cursor.execute(
                        "INSERT INTO pokemon_velocities (pokemon_id, environment_id, quantity) VALUES (?, ?, ?)",
                        (pokemon_id, env_id, int(env_quantity))
                    )
                else:
                    # Si es el entorno Normal, debe tener un valor
                    cursor.execute("SELECT name FROM environments WHERE id = ?", (env_id,))
                    env_name_result = cursor.fetchone()
                    if env_name_result and env_name_result[0] == 'Normal':
                        return False, "La velocidad Normal debe tener un valor mayor que 0"
            
            # Si es una mega evolución, copiar movimientos del pokémon base
            if form_data.get('is_mega') and form_data.get('base_pokemon_id'):
                base_pokemon_id = form_data['base_pokemon_id']
                print(f"🔄 Copiando movimientos del pokémon base ID: {base_pokemon_id}")
                
                # Copiar movimientos por nivel
                cursor.execute("""
                    SELECT movement_id, level 
                    FROM moveset_per_level 
                    WHERE pokemon_id = ?
                """, (base_pokemon_id,))
                level_movements = cursor.fetchall()
                
                for movement in level_movements:
                    cursor.execute(
                        "INSERT INTO moveset_per_level (pokemon_id, movement_id, level) VALUES (?, ?, ?)",
                        (pokemon_id, movement['movement_id'], movement['level'])
                    )
                
                # Copiar learnset completo
                cursor.execute("""
                    SELECT movement_id 
                    FROM learnset 
                    WHERE pokemon_id = ?
                """, (base_pokemon_id,))
                learnset_movements = cursor.fetchall()
                
                for movement in learnset_movements:
                    cursor.execute(
                        "INSERT INTO learnset (pokemon_id, movement_id) VALUES (?, ?)",
                        (pokemon_id, movement['movement_id'])
                    )
                
                print(f"✅ Copiados {len(level_movements)} movimientos por nivel y {len(learnset_movements)} del learnset")
            
            conn.commit()
            
            # Mensaje de éxito personalizado
            if form_data.get('is_mega'):
                success_msg = f"¡Mega {form_data['name']} creada exitosamente con todos los movimientos del pokémon base!"
            elif intercalar:
                success_msg = f"¡Pokémon '{form_data['name']}' intercalado exitosamente en la posición {dex_num}! Se desplazaron {updated_count} pokémons."
            else:
                success_msg = f"¡Pokémon '{form_data['name']}' creado exitosamente!"
            
            return True, success_msg
            
    except Exception as e:
        return False, f"Error al crear el pokémon: {str(e)}"

def get_pokemon_list():
    """Obtiene la lista de todos los pokémons con su información completa"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Obtener pokémons básicos
        cursor.execute("""
            SELECT p.*, s.name as size_name 
            FROM pokemons p 
            JOIN sizes s ON p.size_id = s.id 
            ORDER BY p.dex_num
        """)
        pokemons = cursor.fetchall()
        
        pokemon_list = []
        for pokemon in pokemons:
            # Obtener tipos del pokémon
            cursor.execute("""
                SELECT t.name 
                FROM pokemon_types pt 
                JOIN types t ON pt.type_id = t.id 
                WHERE pt.pokemon_id = ?
            """, (pokemon['id'],))
            types = [row[0] for row in cursor.fetchall()]
            
            # Obtener habilidades del pokémon
            cursor.execute("""
                SELECT a.name 
                FROM pokemon_abilities pa 
                JOIN abilities a ON pa.ability_id = a.id 
                WHERE pa.pokemon_id = ?
            """, (pokemon['id'],))
            abilities = [row[0] for row in cursor.fetchall()]
            
            # Obtener habilidades ocultas del pokémon
            cursor.execute("""
                SELECT a.name 
                FROM pokemon_hidden_abilities pha 
                JOIN abilities a ON pha.ability_id = a.id 
                WHERE pha.pokemon_id = ?
            """, (pokemon['id'],))
            hidden_abilities = [row[0] for row in cursor.fetchall()]
            
            # Obtener hábitats del pokémon
            cursor.execute("""
                SELECT h.name 
                FROM pokemon_habitats ph 
                JOIN habitats h ON ph.habitat_id = h.id 
                WHERE ph.pokemon_id = ?
            """, (pokemon['id'],))
            habitats = [row[0] for row in cursor.fetchall()]
            
            # Obtener proficiencias del pokémon
            cursor.execute("""
                SELECT p.name 
                FROM pokemon_proficiencies pp 
                JOIN proficiencies p ON pp.proficiency_id = p.id 
                WHERE pp.pokemon_id = ?
            """, (pokemon['id'],))
            proficiencies = [row[0] for row in cursor.fetchall()]
            
            # Obtener sentidos del pokémon
            cursor.execute("""
                SELECT s.name, ps.quantity 
                FROM pokemon_senses ps 
                JOIN senses s ON ps.sense_id = s.id 
                WHERE ps.pokemon_id = ?
            """, (pokemon['id'],))
            senses = [f"{row[0]} ({row[1]})" if row[1] else row[0] for row in cursor.fetchall()]
            
            # Obtener velocidades por entorno del pokémon
            cursor.execute("""
                SELECT e.name, pv.quantity 
                FROM pokemon_velocities pv 
                JOIN environments e ON pv.environment_id = e.id 
                WHERE pv.pokemon_id = ?
            """, (pokemon['id'],))
            velocities = [f"{row[0]}: {row[1]}" for row in cursor.fetchall()]
            
            pokemon_dict = dict(pokemon)
            pokemon_dict['type_names'] = types
            pokemon_dict['abilities'] = abilities
            pokemon_dict['hidden_abilities'] = hidden_abilities
            pokemon_dict['habitats'] = habitats
            pokemon_dict['proficiencies'] = proficiencies
            pokemon_dict['senses'] = senses
            pokemon_dict['velocities'] = velocities
            pokemon_list.append(pokemon_dict)
        
        return pokemon_list

@app.route('/', methods=['GET', 'POST'])
def index():
    """Página principal con el formulario de creación"""
    if request.method == 'POST':
        # Crear diccionario de datos del formulario permitiendo listas
        form_data = {}
        
        # Campos individuales (strings)
        for key in ['dex_num', 'name', 'size_id', 'evasion_num', 'evasion_star', 
                   'vitality_num', 'vitality_star', 'strength_num', 'strength_star',
                   'agility_num', 'agility_star', 'endurance_num', 'endurance_star',
                   'mind_num', 'mind_star', 'spirit_num', 'spirit_star',
                   'presence_num', 'presence_star', 'min_level', 'capture_rate',
                   'diet', 'sex', 'description', 'base_pokemon_id']:
            form_data[key] = request.form.get(key, '')
        
        # Campos de checkbox (listas)
        form_data['types'] = request.form.getlist('types')
        form_data['abilities'] = request.form.getlist('abilities')
        form_data['hidden_abilities'] = request.form.getlist('hidden_abilities')
        form_data['habitats'] = request.form.getlist('habitats')
        form_data['proficiencies'] = request.form.getlist('proficiencies')
        form_data['senses'] = request.form.getlist('senses')
        form_data['environments'] = request.form.getlist('environments')
        
        # Campos dinámicos de cantidades (para sentidos y entornos)
        for key, value in request.form.items():
            if key.startswith('sense_quantity_') or key.startswith('env_quantity_'):
                form_data[key] = value
        
        # Obtener información de mega evolución
        form_data['is_mega'] = 'is_mega' in request.form
        form_data['base_pokemon_id'] = form_data.get('base_pokemon_id', None)
        
        # Obtener información de intercalar pokémon
        form_data['intercalar_pokemon'] = 'intercalar_pokemon' in request.form
        
        success, message = create_pokemon(form_data)
        
        # Si es una petición AJAX, devolver JSON
        if request.headers.get('Content-Type') == 'application/json' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': success, 'message': message})
        
        # Para peticiones normales del formulario
        if success:
            return redirect(url_for('index'))
        else:
            # En caso de error, mantener los datos en el formulario
            pass
    
    # Obtener datos para el formulario
    reference_data = get_reference_data()
    return render_template('index.html', **reference_data)

@app.route('/list')
def pokemon_list():
    """Página para listar todos los pokémons"""
    pokemons = get_pokemon_list()
    return render_template('pokemon_list.html', pokemons=pokemons)



@app.route('/api/search_pokemons')
def search_pokemons():
    """API para buscar pokémons existentes"""
    query = request.args.get('q', '').lower()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if query:
            cursor.execute(
                "SELECT id, dex_num, name FROM pokemons WHERE LOWER(name) LIKE ? OR CAST(dex_num AS TEXT) LIKE ? ORDER BY dex_num LIMIT 20",
                (f'%{query}%', f'%{query}%')
            )
        else:
            cursor.execute("SELECT id, dex_num, name FROM pokemons ORDER BY dex_num LIMIT 20")
        
        pokemons = []
        for row in cursor.fetchall():
            pokemons.append({
                'id': row['id'],
                'dex_num': row['dex_num'],
                'name': row['name']
            })
        
        return jsonify(pokemons)

@app.route('/api/pokemon/<int:pokemon_id>')
def get_pokemon_data(pokemon_id):
    """API para obtener todos los datos de un pokémon específico"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Obtener datos básicos del pokémon
        cursor.execute("""
            SELECT p.*, s.name as size_name 
            FROM pokemons p 
            JOIN sizes s ON p.size_id = s.id 
            WHERE p.id = ?
        """, (pokemon_id,))
        pokemon = cursor.fetchone()
        
        if not pokemon:
            return jsonify({'error': 'Pokémon no encontrado'}), 404
        
        # Obtener tipos
        cursor.execute("""
            SELECT t.id, t.name 
            FROM pokemon_types pt 
            JOIN types t ON pt.type_id = t.id 
            WHERE pt.pokemon_id = ?
        """, (pokemon_id,))
        types = cursor.fetchall()
        
        # Obtener habilidades normales
        cursor.execute("""
            SELECT a.id, a.name 
            FROM pokemon_abilities pa 
            JOIN abilities a ON pa.ability_id = a.id 
            WHERE pa.pokemon_id = ?
        """, (pokemon_id,))
        abilities = cursor.fetchall()
        
        # Obtener habilidades ocultas
        cursor.execute("""
            SELECT a.id, a.name 
            FROM pokemon_hidden_abilities pha 
            JOIN abilities a ON pha.ability_id = a.id 
            WHERE pha.pokemon_id = ?
        """, (pokemon_id,))
        hidden_abilities = cursor.fetchall()
        
        # Obtener proficiencias
        cursor.execute("""
            SELECT p.id, p.name 
            FROM pokemon_proficiencies pp 
            JOIN proficiencies p ON pp.proficiency_id = p.id 
            WHERE pp.pokemon_id = ?
        """, (pokemon_id,))
        proficiencies = cursor.fetchall()
        
        # Obtener hábitats
        cursor.execute("""
            SELECT h.id, h.name 
            FROM pokemon_habitats ph 
            JOIN habitats h ON ph.habitat_id = h.id 
            WHERE ph.pokemon_id = ?
        """, (pokemon_id,))
        habitats = cursor.fetchall()
        
        # Obtener sentidos con sus cantidades
        cursor.execute("""
            SELECT s.id, s.name, ps.quantity 
            FROM pokemon_senses ps 
            JOIN senses s ON ps.sense_id = s.id 
            WHERE ps.pokemon_id = ?
        """, (pokemon_id,))
        senses = cursor.fetchall()
        
        # Obtener velocidades por entorno
        cursor.execute("""
            SELECT e.id, e.name, pv.quantity 
            FROM pokemon_velocities pv 
            JOIN environments e ON pv.environment_id = e.id 
            WHERE pv.pokemon_id = ?
        """, (pokemon_id,))
        velocities = cursor.fetchall()
        
        # Obtener movimientos por nivel
        cursor.execute("""
            SELECT m.id, m.name, mpl.level 
            FROM moveset_per_level mpl 
            JOIN movements m ON mpl.movement_id = m.id 
            WHERE mpl.pokemon_id = ? 
            ORDER BY mpl.level, m.name
        """, (pokemon_id,))
        moveset_per_level = cursor.fetchall()
        
        # Obtener learnset
        cursor.execute("""
            SELECT m.id, m.name 
            FROM learnset l 
            JOIN movements m ON l.movement_id = m.id 
            WHERE l.pokemon_id = ? 
            ORDER BY m.name
        """, (pokemon_id,))
        learnset = cursor.fetchall()
        
        return jsonify({
            'pokemon': dict(pokemon),
            'types': [dict(t) for t in types],
            'abilities': [dict(a) for a in abilities],
            'hidden_abilities': [dict(a) for a in hidden_abilities],
            'habitats': [dict(h) for h in habitats],
            'proficiencies': [dict(p) for p in proficiencies],
            'senses': [dict(s) for s in senses],
            'velocities': [dict(v) for v in velocities],
            'moveset_per_level': [dict(m) for m in moveset_per_level],
            'learnset': [dict(m) for m in learnset]
        })



@app.route('/api/pokemon/<int:pokemon_id>/update', methods=['POST'])
def update_pokemon(pokemon_id):
    """API para actualizar un pokémon existente"""
    try:
        data = request.get_json()
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Actualizar datos básicos
            cursor.execute("""
                UPDATE pokemons SET 
                    name = ?, dex_num = ?, size_id = ?, hit_points = ?, 
                    strength = ?, strength_stars = ?, dexterity = ?, dexterity_stars = ?, 
                    constitution = ?, constitution_stars = ?, intelligence = ?, intelligence_stars = ?, 
                    wisdom = ?, wisdom_stars = ?, charisma = ?, charisma_stars = ?, 
                    walk_speed = ?, run_speed = ?, swim_speed = ?, climb_speed = ?, 
                    fly_speed = ?, dig_speed = ?, levitate_speed = ?, 
                    description = ?, legendary = ?
                WHERE id = ?
            """, (
                data['name'], data['dex_num'], data['size_id'], data['hit_points'],
                data['strength'], data['strength_stars'], data['dexterity'], data['dexterity_stars'],
                data['constitution'], data['constitution_stars'], data['intelligence'], data['intelligence_stars'],
                data['wisdom'], data['wisdom_stars'], data['charisma'], data['charisma_stars'],
                data['walk_speed'], data['run_speed'], data['swim_speed'], data['climb_speed'],
                data['fly_speed'], data['dig_speed'], data['levitate_speed'],
                data['description'], data.get('legendary', 0), pokemon_id
            ))
            
            # Limpiar relaciones existentes
            cursor.execute("DELETE FROM pokemon_types WHERE pokemon_id = ?", (pokemon_id,))
            cursor.execute("DELETE FROM pokemon_abilities WHERE pokemon_id = ?", (pokemon_id,))
            cursor.execute("DELETE FROM pokemon_hidden_abilities WHERE pokemon_id = ?", (pokemon_id,))
            cursor.execute("DELETE FROM pokemon_proficiencies WHERE pokemon_id = ?", (pokemon_id,))
            
            # Insertar tipos
            if 'types' in data:
                for type_id in data['types']:
                    cursor.execute("INSERT INTO pokemon_types (pokemon_id, type_id) VALUES (?, ?)", (pokemon_id, type_id))
            
            # Insertar habilidades normales
            if 'abilities' in data:
                for ability_id in data['abilities']:
                    cursor.execute("INSERT INTO pokemon_abilities (pokemon_id, ability_id) VALUES (?, ?)", (pokemon_id, ability_id))
            
            # Insertar habilidades ocultas
            if 'hidden_abilities' in data:
                for ability_id in data['hidden_abilities']:
                    cursor.execute("INSERT INTO pokemon_hidden_abilities (pokemon_id, ability_id) VALUES (?, ?)", (pokemon_id, ability_id))
            
            # Insertar proficiencias
            if 'proficiencies' in data:
                for prof_id in data['proficiencies']:
                    cursor.execute("INSERT INTO pokemon_proficiencies (pokemon_id, proficiency_id) VALUES (?, ?)", (pokemon_id, prof_id))
            
            conn.commit()
            return jsonify({'success': True, 'message': 'Pokémon actualizado correctamente'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400



@app.errorhandler(404)
def not_found_error(error):
    return "Página no encontrada", 404

@app.errorhandler(500)
def internal_error(error):
    return "Error interno del servidor", 500

if __name__ == '__main__':
    # Verificar que la base de datos existe
    if not os.path.exists(DB_PATH):
        print(f"❌ Error: No se encontró la base de datos en {DB_PATH}")
        print("Asegúrate de que el archivo pokeRol.db existe en la raíz del proyecto.")
        exit(1)
    
    # Inicializar la base de datos con datos básicos
    print("🔄 Inicializando base de datos...")
    init_database()
    print("✅ Base de datos inicializada correctamente")
    
    print("🚀 Iniciando servidor PokéRol...")
    print("📱 Accede a: http://localhost:5000")
    print("📋 Lista de pokémons: http://localhost:5000/list")
    print("⚡ Presiona Ctrl+C para detener el servidor")
    
    app.run(debug=True, host='0.0.0.0', port=5000)