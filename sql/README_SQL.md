# 🗃️ GUÍA PARA LA BASE DE DATOS

## Esquema de CEDIZA

La base de datos tiene **14 tablas** interrelacionadas.

---

## 🚀 CÓMO EJECUTAR LOS SCRIPTS

```bash
# Terminal MySQL
mysql -u root -p < sql/init.sql
```

## ERR diagram

El diagrama relacional de la base de datos guardado como **ERR_diagram.png**

---

## 📊 TABLAS

| Tabla | Descripción |
|-------|-------------|
| Usuarios | Datos comunes de todos los usuarios (base) |
| Pacientes | Extiende Usuarios |
| Pac_pri | Pacientes privados — extiende Pacientes (IVA, cuenta, horas) |
| Pac_pub | Pacientes públicos — extiende Pacientes (días ingresado en hospital) |
| Trabajadores | Extiende Usuarios |
| Auxiliares | Extiende Trabajadores (horario) |
| coordinadores | Extiende Trabajadores (infoInteres) |
| Especialistas | Extiende Trabajadores (especialidad, horario) |
| Familiares | Contactos asociados a un paciente |
| comentarios | Anotaciones libres de los trabajadores a los pacientes |
| Sesion | Sesión terapéutica entre un especialista y un paciente |
| Cuestionarios | Cuestionarios disponibles en el sistema |
| Preguntas | Preguntas asociadas a cada cuestionario |
| Respuestas | Respuestas de los pacientes a las preguntas |

---

## 🔑 RELACIONES CLAVE

- Paciente 1:N Familiares
- Paciente 1:N comentarios
- Trabajador 1:N comentarios
- Especialista 1:N Sesiones
- Paciente 1:N Sesiones
- Cuestionario 1:N Preguntas
- Pregunta 1:N Respuestas
- Paciente 1:N Respuestas