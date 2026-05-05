# 🗃️ GUÍA PARA LA BASE DE DATOS

## Esquema de CEDIZA

La base de datos tiene **11 tablas** interrelacionadas.

---

## 🚀 CÓMO EJECUTAR LOS SCRIPTS

```bash
# Terminal MySQL
mysql -u root -p < sql/init.sql
```

## ERR diagram 

El diagrama relacional de la base de datos guardado como **ERR_diagram.png**

## 📊 TABLAS

| Tabla | Descripción |
|-------|-------------|
| Usuarios | Datos comunes de todos los usuarios (base) |
| Pacientes | Extiende Usuarios |
| Pacientes privados | Extiende Pacientes |
| Pacientes publicos | Extiende Pacientes |
| Trabajadores | Extiende Usuarios |
| Auxiliares | Extiende Trabajadores |
| coordinadores | Extiende Trabajadores |
| Especialistas | Extiende Trabajadores |
| Familiares | Contactos asociados a un paciente |
| comentarios | Anotaciones libres de los trabajadores a los pacientes |
| Sesiones | sesion entre un especialista y un paciente |


## 🔑 RELACIONES CLAVE

- Paciente 1:N Familiares
- Paciente 1:N comentarios
- Trabajador 1:N comentarios
- Sesion 1:N pacientes
- Sesion 1:N especialistas