// PokéRol - Sistema de formulario de Pokemon
// Funcionalidades: Limitación de checkboxes, mega evolución, intercalar pokemon

// Función para limitar la selección de checkboxes
function limitCheckboxSelection(checkboxName, maxLimit, groupName) {
    const checkboxes = document.querySelectorAll(`input[name="${checkboxName}"]`);
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const checkedBoxes = document.querySelectorAll(`input[name="${checkboxName}"]:checked`);
            
            if (checkedBoxes.length >= maxLimit) {
                // Deshabilitar los checkboxes no seleccionados
                checkboxes.forEach(cb => {
                    if (!cb.checked) {
                        cb.disabled = true;
                        cb.parentElement.style.opacity = '0.5';
                    }
                });
                
                // Mostrar mensaje de advertencia
                showLimitWarning(groupName, maxLimit);
            } else {
                // Rehabilitar todos los checkboxes
                checkboxes.forEach(cb => {
                    cb.disabled = false;
                    cb.parentElement.style.opacity = '1';
                });
                
                // Ocultar mensaje de advertencia
                hideLimitWarning(groupName);
            }
        });
    });
}

function showLimitWarning(groupName, maxLimit) {
    const existingWarning = document.getElementById(`warning-${groupName}`);
    if (existingWarning) return;
    
    const warningDiv = document.createElement('div');
    warningDiv.id = `warning-${groupName}`;
    warningDiv.className = 'limit-warning';
    warningDiv.innerHTML = `⚠️ Máximo ${maxLimit} ${groupName} permitido${maxLimit > 1 ? 's' : ''}`;
    
    const groupContainer = document.querySelector(`input[name="${groupName}"]`).closest('.form-group');
    if (groupContainer) {
        groupContainer.appendChild(warningDiv);
    }
}

function hideLimitWarning(groupName) {
    const warning = document.getElementById(`warning-${groupName}`);
    if (warning) {
        warning.remove();
    }
}

// Función para buscar pokémons
function searchPokemons(query, searchResults) {
    if (query.length === 0) {
        searchResults.style.display = 'none';
        return;
    }
    
    searchResults.innerHTML = '<div class="search-loading">Buscando...</div>';
    searchResults.style.display = 'block';
    
    fetch(`/api/search_pokemons?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            searchResults.innerHTML = '';
            
            if (data.length === 0) {
                searchResults.innerHTML = '<div class="search-no-results">No se encontraron pokémons</div>';
                return;
            }
            
            data.forEach(pokemon => {
                const item = document.createElement('div');
                item.className = 'search-result-item';
                item.innerHTML = `
                    <span class="search-result-name">${pokemon.name}</span>
                    <span class="search-result-dex">#${pokemon.dex_num}</span>
                `;
                
                item.addEventListener('click', function() {
                    loadPokemonData(pokemon.id);
                    searchResults.style.display = 'none';
                    const searchInput = document.getElementById('pokemon-search');
                    if (searchInput) {
                        searchInput.value = `${pokemon.name} (#${pokemon.dex_num})`;
                    }
                    // Guardar el ID del pokémon base para la creación de la mega evolución
                    const baseIdInput = document.getElementById('base_pokemon_id');
                    if (baseIdInput) {
                        baseIdInput.value = pokemon.id;
                    }
                });
                
                searchResults.appendChild(item);
            });
        })
        .catch(error => {
            console.error('Error buscando pokémons:', error);
            searchResults.innerHTML = '<div class="search-no-results">Error en la búsqueda</div>';
        });
}

// Función para cargar datos de un pokémon completa
function loadPokemonData(pokemonId) {
    fetch(`/api/pokemon/${pokemonId}`)
        .then(response => response.json())
        .then(data => {
            console.log('Datos completos recibidos:', data);
            const pokemon = data.pokemon || data; // Acceder al objeto pokemon dentro de data
            
            console.log('Cargando datos del pokémon:', pokemon);
            
            // Llenar campos básicos
            if (pokemon.size_id) {
                const sizeSelect = document.getElementById('size_id');
                if (sizeSelect) {
                    sizeSelect.value = pokemon.size_id;
                    console.log('Tamaño seleccionado:', pokemon.size_id);
                } else {
                    console.error('No se encontró el select de tamaño');
                }
            }
            
            if (pokemon.diet) {
                const dietInput = document.getElementById('diet');
                if (dietInput) {
                    dietInput.value = pokemon.diet;
                    console.log('Dieta cargada:', pokemon.diet);
                }
            }
            if (pokemon.sex) {
                const sexInput = document.getElementById('sex');
                if (sexInput) {
                    sexInput.value = pokemon.sex;
                    console.log('Sexo cargado:', pokemon.sex);
                }
            }
            
            // Llenar estadísticas
            fillStatField('evasion', pokemon.evasion);
            fillStatField('vitality', pokemon.vitality);
            fillStatField('strength', pokemon.strength);
            fillStatField('agility', pokemon.agility);
            fillStatField('endurance', pokemon.endurance);
            fillStatField('mind', pokemon.mind);
            fillStatField('spirit', pokemon.spirit);
            fillStatField('presence', pokemon.presence);
            
            // Otros campos numéricos
            if (pokemon.min_level !== undefined && pokemon.min_level !== null) {
                const minLevelInput = document.getElementById('min_level');
                if (minLevelInput) {
                    minLevelInput.value = pokemon.min_level;
                    console.log('Nivel mínimo cargado:', pokemon.min_level);
                } else {
                    console.error('No se encontró el input de nivel mínimo');
                }
            } else {
                console.warn('min_level no definido en los datos del pokémon');
            }
            
            if (pokemon.capture_rate !== undefined && pokemon.capture_rate !== null) {
                const captureRateInput = document.getElementById('capture_rate');
                if (captureRateInput) {
                    captureRateInput.value = pokemon.capture_rate;
                    console.log('Ratio de captura cargado:', pokemon.capture_rate);
                } else {
                    console.error('No se encontró el input de ratio de captura');
                }
            } else {
                console.warn('capture_rate no definido en los datos del pokémon');
            }
            
            // Seleccionar tipos
            document.querySelectorAll('input[name="types"]').forEach(checkbox => {
                checkbox.checked = false;
            });
            if (data.types) {
                data.types.forEach(type => {
                    const typeCheckbox = document.querySelector(`input[name="types"][value="${type.id}"]`);
                    if (typeCheckbox) typeCheckbox.checked = true;
                });
            }
            
            // Seleccionar habilidades
            document.querySelectorAll('input[name="abilities"]').forEach(checkbox => {
                checkbox.checked = false;
            });
            if (data.abilities) {
                data.abilities.forEach(ability => {
                    const abilityCheckbox = document.querySelector(`input[name="abilities"][value="${ability.id}"]`);
                    if (abilityCheckbox) abilityCheckbox.checked = true;
                });
            }
            
            // Seleccionar habilidades ocultas
            document.querySelectorAll('input[name="hidden_abilities"]').forEach(checkbox => {
                checkbox.checked = false;
            });
            if (data.hidden_abilities) {
                data.hidden_abilities.forEach(ability => {
                    const hiddenAbilityCheckbox = document.querySelector(`input[name="hidden_abilities"][value="${ability.id}"]`);
                    if (hiddenAbilityCheckbox) hiddenAbilityCheckbox.checked = true;
                });
            }
            
            // Seleccionar hábitats
            document.querySelectorAll('input[name="habitats"]').forEach(checkbox => {
                checkbox.checked = false;
            });
            if (data.habitats) {
                data.habitats.forEach(habitat => {
                    const habitatCheckbox = document.querySelector(`input[name="habitats"][value="${habitat.id}"]`);
                    if (habitatCheckbox) habitatCheckbox.checked = true;
                });
            }
            
            // Seleccionar proficiencias
            document.querySelectorAll('input[name="proficiencies"]').forEach(checkbox => {
                checkbox.checked = false;
            });
            if (data.proficiencies) {
                data.proficiencies.forEach(proficiency => {
                    const profCheckbox = document.querySelector(`input[name="proficiencies"][value="${proficiency.id}"]`);
                    if (profCheckbox) profCheckbox.checked = true;
                });
            }
            
            // Llenar sentidos
            document.querySelectorAll('input[name="senses"]').forEach(checkbox => {
                checkbox.checked = false;
            });
            document.querySelectorAll('.sense-quantity').forEach(input => {
                input.value = '';
            });
            if (data.senses && data.senses.length > 0) {
                console.log('Cargando sentidos:', data.senses);
                data.senses.forEach(sense => {
                    // Marcar el checkbox del sentido
                    const senseCheckbox = document.querySelector(`input[name="senses"][value="${sense.id}"]`);
                    if (senseCheckbox) {
                        senseCheckbox.checked = true;
                        console.log(`Sentido marcado: ${sense.name}`);
                    }
                    
                    // Llenar la cantidad del sentido
                    const senseQuantityInput = document.getElementById(`sense_quantity_${sense.id}`);
                    if (senseQuantityInput && sense.quantity) {
                        senseQuantityInput.value = sense.quantity;
                        console.log(`Cantidad del sentido ${sense.name}: ${sense.quantity}`);
                    }
                });
            }
            
            // Seleccionar entornos y llenar velocidades
            document.querySelectorAll('input[name="environments"]').forEach(checkbox => {
                checkbox.checked = false;
            });
            document.querySelectorAll('.env-quantity').forEach(input => {
                input.value = '';
            });
            if (data.velocities && data.velocities.length > 0) {
                data.velocities.forEach(velocity => {
                    const envCheckbox = document.querySelector(`input[name="environments"][value="${velocity.id}"]`);
                    if (envCheckbox) {
                        envCheckbox.checked = true;
                    }
                    const envQuantityInput = document.getElementById(`env_quantity_${velocity.id}`);
                    if (envQuantityInput && velocity.quantity) {
                        envQuantityInput.value = velocity.quantity;
                    }
                });
            }
            
            // Llenar descripción
            if (pokemon.description) {
                const descriptionInput = document.getElementById('description');
                if (descriptionInput) descriptionInput.value = pokemon.description;
            }
            
            // Cargar movimientos
            loadPokemonMovements(data);
            
            console.log(`🎉 Datos de ${pokemon.name} cargados correctamente`);
            console.log('Todos los campos se han rellenado automáticamente');
        })
        .catch(error => {
            console.error('Error cargando datos del pokémon:', error);
            console.error('Error al cargar los datos del pokémon');
        });
}

// Función auxiliar para llenar campos de estadísticas
function fillStatField(statName, statValue) {
    if (!statValue) return;
    
    console.log(`Procesando estadística ${statName}:`, statValue);
    
    const valueStr = statValue.toString();
    let number = '';
    let star = '';
    
    // Para evasión y vitalidad, no hay estrellas, solo texto
    if (statName === 'evasion' || statName === 'vitality') {
        number = valueStr.trim();
        star = ''; // Sin estrella
    } else {
        // Para las demás estadísticas: buscar estrella al final
        if (valueStr.includes(' ☆')) {
            const parts = valueStr.split(' ☆');
            number = parts[0].trim();
            star = ' ☆';
        } else if (valueStr.includes(' ★')) {
            const parts = valueStr.split(' ★');
            number = parts[0].trim();
            star = ' ★';
        } else {
            number = valueStr.trim();
            star = ''; // Sin estrella
        }
    }
    
    const numberInput = document.getElementById(`${statName}_num`);
    const starSelect = document.getElementById(`${statName}_star`);
    
    if (numberInput) {
        numberInput.value = number;
        console.log(`Campo ${statName}_num llenado con:`, number);
    } else {
        console.error(`No se encontró el input ${statName}_num`);
    }
    
    // Solo intentar llenar el select de estrella si no es evasión ni vitalidad
    if (starSelect && statName !== 'evasion' && statName !== 'vitality') {
        starSelect.value = star;
        console.log(`Campo ${statName}_star llenado con:`, star);
    }
}

// Función para cargar movimientos del pokémon
function loadPokemonMovements(data) {
    const movesetPerLevelContainer = document.getElementById('moveset-per-level');
    if (movesetPerLevelContainer) {
        movesetPerLevelContainer.innerHTML = '';
        
        if (data.moveset_per_level && data.moveset_per_level.length > 0) {
            data.moveset_per_level.forEach(movement => {
                const movementItem = document.createElement('div');
                movementItem.className = 'movement-item';
                movementItem.innerHTML = `
                    <span class="movement-name">${movement.name}</span>
                    <div>
                        <span class="movement-level">Nv. ${movement.level}</span>
                        <span class="movement-type">${movement.type_name || 'Normal'}</span>
                    </div>
                `;
                movesetPerLevelContainer.appendChild(movementItem);
            });
        } else {
            movesetPerLevelContainer.innerHTML = '<p style="text-align: center; color: #666; font-style: italic;">No hay movimientos por nivel registrados.</p>';
        }
    }
    
    const learnsetContainer = document.getElementById('learnset');
    if (learnsetContainer) {
        learnsetContainer.innerHTML = '';
        
        if (data.learnset && data.learnset.length > 0) {
            data.learnset.forEach(movement => {
                const movementItem = document.createElement('div');
                movementItem.className = 'movement-item';
                movementItem.innerHTML = `
                    <span class="movement-name">${movement.name}</span>
                    <span class="movement-type">${movement.type_name || 'Normal'}</span>
                `;
                learnsetContainer.appendChild(movementItem);
            });
        } else {
            learnsetContainer.innerHTML = '<p style="text-align: center; color: #666; font-style: italic;">No hay movimientos en el learnset.</p>';
        }
    }
}

// Función principal de inicialización
document.addEventListener('DOMContentLoaded', function() {
    // Aplicar limitaciones de checkbox
    limitCheckboxSelection('types', 2, 'tipos');
    limitCheckboxSelection('abilities', 3, 'habilidades');
    limitCheckboxSelection('hidden_abilities', 2, 'habilidades ocultas');
    limitCheckboxSelection('proficiencies', 2, 'proficiencias');
    
    // Sistema de Intercalar Pokemon
    const intercalarCheckbox = document.getElementById('intercalar_pokemon');
    const dexNumInput = document.getElementById('dex_num');
    
    console.log('Intercalar checkbox:', intercalarCheckbox);
    console.log('Dex num input:', dexNumInput);
    
    // Manejar el checkbox de intercalar
    if (intercalarCheckbox) {
        console.log('Checkbox intercalar encontrado correctamente');
        
        intercalarCheckbox.addEventListener('change', function() {
            console.log('Intercalar checkbox cambiado:', this.checked);
            
            // Si se marca intercalar, desmarcar mega evolución
            if (this.checked) {
                const megaCheckbox = document.getElementById('is_mega');
                if (megaCheckbox && megaCheckbox.checked) {
                    megaCheckbox.checked = false;
                    const searchContainer = document.getElementById('pokemon-search-container');
                    const movementsSection = document.getElementById('movements-section');
                    if (searchContainer) searchContainer.style.display = 'none';
                    if (movementsSection) movementsSection.style.display = 'none';
                    console.log('Mega evolución desmarcada automáticamente');
                }
            }
        });
    } else {
        console.error('No se pudo encontrar el checkbox de intercalar');
    }
    
    // Sistema de Mega Evolución
    const megaCheckbox = document.getElementById('is_mega');
    const searchContainer = document.getElementById('pokemon-search-container');
    const movementsSection = document.getElementById('movements-section');
    const searchInput = document.getElementById('pokemon-search');
    const searchResults = document.getElementById('search-results');
    let searchTimeout;
    
    // Verificar que todos los elementos existan
    console.log('Mega checkbox:', megaCheckbox);
    console.log('Search container:', searchContainer);
    console.log('Movements section:', movementsSection);
    console.log('Search input:', searchInput);
    console.log('Search results:', searchResults);
    
    // Verificar si alguno es null
    if (!megaCheckbox) {
        console.error('❌ ERROR: megaCheckbox no encontrado');
        return;
    }
    if (!searchContainer) {
        console.error('❌ ERROR: searchContainer no encontrado');
        return;
    }
    if (!movementsSection) {
        console.error('❌ ERROR: movementsSection no encontrado');
        return;
    }
    
    // Event listener del checkbox de mega evolución
    megaCheckbox.addEventListener('change', function() {
        console.log('✅ Mega checkbox changed:', this.checked);
        if (this.checked) {
            // Desmarcar intercalar si está marcado
            if (intercalarCheckbox && intercalarCheckbox.checked) {
                intercalarCheckbox.checked = false;
            }
            
            console.log('Mostrando search container y movements section');
            searchContainer.style.display = 'block';
            movementsSection.style.display = 'block';
            console.log('✨ Sistema de mega evolución activado');
        } else {
            console.log('Ocultando search container y movements section');
            searchContainer.style.display = 'none';
            movementsSection.style.display = 'none';
            if (searchResults) {
                searchResults.style.display = 'none';
                searchResults.innerHTML = '';
            }
            // Limpiar movimientos
            const movesetContainer = document.getElementById('moveset-per-level');
            const learnsetContainer = document.getElementById('learnset');
            if (movesetContainer) movesetContainer.innerHTML = '';
            if (learnsetContainer) learnsetContainer.innerHTML = '';
            // Limpiar el ID del pokémon base
            const baseIdInput = document.getElementById('base_pokemon_id');
            if (baseIdInput) baseIdInput.value = '';
            // Limpiar el campo de búsqueda
            if (searchInput) searchInput.value = '';
            console.log('Sistema de mega evolución desactivado');
        }
    });
    
    // Event listeners para búsqueda
    if (searchInput && searchResults) {
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            searchTimeout = setTimeout(() => {
                searchPokemons(query, searchResults);
            }, 300);
        });
        
        document.addEventListener('click', function(event) {
            if (!searchContainer.contains(event.target)) {
                searchResults.style.display = 'none';
            }
        });
    }
    
    // Validación de formulario antes del envío
    const form = document.querySelector('.pokemon-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault(); // Prevenir envío normal
            
            let errors = [];
            
            // Validar que al menos 1 tipo esté seleccionado
            const typesChecked = document.querySelectorAll('input[name="types"]:checked').length;
            if (typesChecked === 0) {
                errors.push('Debes seleccionar al menos 1 tipo');
            }
            
            // Validar que al menos 1 habilidad esté seleccionada
            const abilitiesChecked = document.querySelectorAll('input[name="abilities"]:checked').length;
            if (abilitiesChecked === 0) {
                errors.push('Debes seleccionar al menos 1 habilidad');
            }
            
            // Validar que al menos 1 hábitat esté seleccionado
            const habitatsChecked = document.querySelectorAll('input[name="habitats"]:checked').length;
            if (habitatsChecked === 0) {
                errors.push('Debes seleccionar al menos 1 hábitat');
            }
            
            // Verificar que velocidad Normal esté marcada
            const normalEnvChecked = Array.from(document.querySelectorAll('input[name="environments"]:checked'))
                .some(checkbox => {
                    const envItem = checkbox.closest('.env-item');
                    if (envItem) {
                        const label = envItem.querySelector('label');
                        if (label) {
                            return label.textContent.trim().includes('Normal');
                        }
                    }
                    return false;
                });
            
            if (!normalEnvChecked) {
                errors.push('Debe seleccionar la velocidad Normal');
            }
            
            // Mostrar errores si los hay
            if (errors.length > 0) {
                console.error('Errores encontrados:', errors);
                alert('Errores encontrados:\n• ' + errors.join('\n• '));
                return false;
            }
            
            // Si no hay errores, enviar por AJAX
            const formData = new FormData(form);
            
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('✅ ' + data.message);
                    form.reset(); // Limpiar formulario
                    // Ocultar secciones de mega evolución si estaban visibles
                    if (searchContainer) searchContainer.style.display = 'none';
                    if (movementsSection) movementsSection.style.display = 'none';
                } else {
                    alert('❌ Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('❌ Error de conexión. Inténtalo de nuevo.');
            });
        });
    }
});