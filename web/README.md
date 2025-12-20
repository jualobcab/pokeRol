# 🎲 PokéRol - Aplicación Web

> **Aplicación web profesional para crear y gestionar pokémons en el sistema PokéRol usando Flask**

Una herramienta completa que permite crear pokémons personalizados con todas sus características, estadísticas, habilidades y más, incluyendo un sistema avanzado de **Mega Evoluciones** que facilita la creación de variantes basadas en pokémons existentes.

---

## ✨ Características Principales

### 🎯 **Creación Completa de Pokémons**
- **Formulario intuitivo** con todos los campos del sistema PokéRol
- **Validación inteligente** de datos en tiempo real
- **Estadísticas con formato especial** (número + estrellas ☆★)
- **Selección múltiple** para tipos, habilidades, hábitats y proficiencias

### ⭐ **Sistema de Mega Evolución**
- **Búsqueda inteligente** de pokémons base por nombre o número
- **Carga automática** de todos los datos del pokémon seleccionado
- **Personalización completa** de estadísticas y características del Mega
- **Interfaz tipo dropdown** con resultados en tiempo real

### 🎨 **Interfaz Moderna**
- **Diseño responsive** que se adapta a cualquier dispositivo
- **Tema visual Pokémon** con gradientes y efectos modernos
- **Iconos emoji** para mejor experiencia de usuario
- **Validaciones visuales** con mensajes informativos

### 📊 **Gestión Avanzada**
- **Lista visual** de todos los pokémons creados
- **Tarjetas informativas** con datos completos
- **Búsqueda y filtrado** de pokémons existentes
- **API REST** para integración con otros sistemas

---

## 🚀 Inicio Rápido

### **Ejecución Automática (Recomendado)**
```bash
# Desde la raíz del proyecto
ejecutar_web.bat
```

### **Ejecución Manual**
```bash
cd web/
pip install -r requirements.txt
python app.py
```

**🌐 Accede a:** `http://localhost:5000`

---

## 📋 Funcionalidades Detalladas

### **🎮 Creación de Pokémons**

#### Campos Obligatorios
- **Identificación**: Nombre, Número de Pokédex
- **Características**: Tamaño, Tipos (1-2)
- **Estadísticas**: Evasión, Vitalidad, Fuerza, Agilidad, Resistencia, Mente, Espíritu, Presencia
- **Combate**: Nivel mínimo, Ratio de captura
- **Entorno**: Hábitats, Velocidad "Normal" obligatoria

#### Campos Opcionales
- **Habilidades**: Normales (máx. 3) y Ocultas (máx. 2)
- **Características**: Dieta, Sexo, Descripción
- **Habilidades**: Proficiencias (máx. 2)
- **Sentidos**: Con cantidades específicas

### **⭐ Sistema de Mega Evolución**

1. **Activar Mega**: Marca el checkbox "Este es un Mega Pokémon ⭐"
2. **Buscar Base**: Escribe el nombre o número del pokémon base
3. **Seleccionar**: Click en el pokémon de los resultados
4. **Personalizar**: Todos los datos se cargan automáticamente
5. **Modificar**: Ajusta nombre, número, estadísticas según la Mega
6. **Crear**: Guarda tu nueva Mega Evolución

### **📊 Validaciones Inteligentes**

- **Límites de selección**: Máx. 2 tipos, 3 habilidades normales, 2 ocultas
- **Campos obligatorios**: Validación en tiempo real
- **Números únicos**: No duplicar números de Pokédex
- **Formato correcto**: Estadísticas, velocidades, cantidades

---

## 🎯 Guía de Uso

### **Crear Pokémon Normal**
1. Ve a `http://localhost:5000`
2. Completa todos los campos obligatorios
3. Selecciona tipos, habilidades, hábitats
4. Ajusta estadísticas y velocidades
5. Click "🎯 Crear Pokémon"

### **Crear Mega Evolución**
1. Marca "Este es un Mega Pokémon ⭐"
2. Busca el pokémon base (ej: "Charizard")
3. Selecciona de la lista
4. Cambia el nombre (ej: "Mega Charizard X")
5. Asigna nuevo número de Pokédex
6. Ajusta estadísticas mejoradas
7. Click "🎯 Crear Pokémon"

### **Ver Lista de Pokémons**
- **URL**: `http://localhost:5000/list`
- **Contenido**: Tarjetas con información completa
- **Navegación**: Botón "➕ Crear Nuevo" para volver al formulario

---

## 🛠️ Especificaciones Técnicas

### **Requisitos**
- **Python**: 3.7 o superior
- **Flask**: 3.0.0
- **Base de datos**: SQLite3 (`pokeRol.db`)
- **Navegador**: Moderno con soporte JavaScript

### **Arquitectura**
```
web/
├── 📄 app.py                    # Aplicación Flask principal
├── 📄 requirements.txt          # Dependencias Python
├── 📁 templates/
│   ├── 📄 index.html           # Formulario principal
│   └── 📄 pokemon_list.html    # Lista de pokémons
├── 📁 static/
│   ├── 📄 style.css            # Estilos CSS
│   └── 📄 pokemon-form.js      # JavaScript del formulario
└── 📄 README.md                # Esta documentación
```

### **API Endpoints**
- **GET /**: Formulario principal
- **POST /**: Crear pokémon
- **GET /list**: Lista de pokémons
- **GET /api/search_pokemons**: Búsqueda de pokémons
- **GET /api/pokemon/{id}**: Datos completos de pokémon

### **Base de Datos**
- **Inicialización automática** desde archivos JSON
- **Más de 350 habilidades** disponibles
- **59 hábitats** diferentes
- **22 proficiencias** de habilidades
- **16 tipos de sentidos** especiales

---

## 🎨 Características Visuales

### **Diseño**
- **Gradientes modernos** inspirados en Pokémon
- **Tarjetas con sombras** y efectos hover
- **Iconos emoji** para mejor UX
- **Colores temáticos** por tipos de pokémon

### **Responsividad**
- **Móvil**: Formulario adaptado a pantallas pequeñas
- **Tablet**: Grid optimizado para tablets
- **Desktop**: Experiencia completa con todas las funciones

### **Interactividad**
- **Validación en tiempo real**
- **Búsqueda instantánea** (300ms debounce)
- **Feedback visual** para acciones del usuario
- **Mensajes informativos** y de error

---

## ⚙️ Configuración Avanzada

### **Modo Desarrollo**
```python
# En app.py
app.run(debug=True, host='0.0.0.0', port=5000)
```

### **Variables de Entorno**
- **DEBUG**: `True` para desarrollo
- **HOST**: `0.0.0.0` para acceso externo
- **PORT**: `5000` por defecto

### **Base de Datos**
- **Ruta**: `../pokeRol.db` (relativa al directorio web)
- **Tipo**: SQLite3 con row_factory
- **Inicialización**: Automática desde JSON

---

## 🚨 Consideraciones Importantes

### **Desarrollo vs Producción**
- ⚠️ **Solo para desarrollo**: No usar en producción
- 🔒 **Seguridad**: Cambiar `secret_key` para producción
- 🐛 **Debug activo**: Recarga automática y errores detallados

### **Compatibilidad**
- ✅ **Compatible** con sistema de scraping existente
- ✅ **Misma base de datos** que otros módulos
- ✅ **No interfiere** con otros componentes

### **Limitaciones**
- 🔄 **Sin edición**: Solo creación de pokémons
- 📊 **Sin análisis**: No incluye estadísticas de uso
- 🔍 **Sin filtros avanzados** en la lista

---

## 🤝 Contribución

Este proyecto forma parte del sistema **PokéRol** y mantiene compatibilidad completa con:
- **Módulo de scraping** para obtener datos oficiales
- **Base de datos compartida** con estructura normalizada
- **Sistema de validaciones** consistente en todo el proyecto

**Para más información sobre el proyecto completo, consulta el README principal en la raíz del repositorio.**