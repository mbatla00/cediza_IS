# 🗃️ GUÍA PARA LA BASE DE DATOS

## Esquema de CEDIZA

La base de datos tiene **9 tablas** interrelacionadas.

---

## 🚀 CÓMO EJECUTAR LOS SCRIPTS

```bash
# Terminal MySQL
mysql -u root -p < sql/schema.sql
mysql -u root -p < sql/inserts_test.sql
```

## 📊 TABLAS

| Tabla | Descripción |
|-------|-------------|
| Usuario | Datos comunes de todos los usuarios (base) |
| Paciente | Extiende Usuario + datos médicos |
| Trabajador | Extiende Usuario + especialidad |
| ContactoEmergencia | Contactos asociados a un paciente |
| PreguntaDiaria | Preguntas predefinidas del cuestionario |
| Respuesta | Respuestas de pacientes a preguntas |
| NotaLibre | Anotaciones libres de trabajadores |
| EvaluacionProfesional | Evaluaciones con puntuaciones 1-5 |
| InformeGenerado | Metadatos de informes PDF |

## 🔑 RELACIONES CLAVE

- Paciente 1:N ContactoEmergencia
- Paciente 1:N Respuesta
- Paciente 1:N NotaLibre
- Paciente 1:N EvaluacionProfesional
- PreguntaDiaria 1:N Respuesta
- Trabajador 1:N NotaLibre
- Trabajador 1:N EvaluacionProfesional