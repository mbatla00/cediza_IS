# 🗃️ GUÍA PARA LA BASE DE DATOS

## Esquema de CEDIZA

La base de datos tiene **17 tablas** interrelacionadas.

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
| Usuarios | Datos comunes de todos los usuarios (base) — incluye `nombre`, `email`, `activo` |
| Pacientes | Extiende Usuarios — incluye `fechaNacimiento`, `foto`, `diagnostico` |
| Pac_pri | Pacientes privados — extiende Pacientes (IVA, cuenta, horas) |
| Pac_pub | Pacientes públicos — extiende Pacientes (días ingresado en hospital externo) |
| Trabajadores | Extiende Usuarios |
| Auxiliares | Extiende Trabajadores (horario) |
| coordinadores | Extiende Trabajadores (infoInteres) |
| Especialistas | Extiende Trabajadores (especialidad, horario) |
| Administrador | Extiende Usuarios — gestiona facturas |
| Familiares | Contactos de emergencia asociados a un paciente |
| comentarios | Anotaciones libres de los trabajadores a los pacientes |
| Sesion | Sesión terapéutica entre un especialista y un paciente |
| EvaluacionProfesional | Evaluación periódica de un paciente realizada por un trabajador |
| Informe | Informe generado por un trabajador sobre un paciente en un periodo |
| Factura | Factura de un paciente gestionada por un administrador |
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
- Trabajador 1:N EvaluacionProfesional
- Paciente 1:N EvaluacionProfesional
- Trabajador 1:N Informe
- Paciente 1:N Informe
- Administrador 1:N Factura
- Paciente 1:N Factura
- Cuestionario 1:N Preguntas
- Pregunta 1:N Respuestas
- Paciente 1:N Respuestas

---

## 📝 CAMBIOS RESPECTO A LA VERSIÓN ANTERIOR

- `Usuarios` ahora tiene `email` y `activo`; `contraseña` renombrado a `password`
- `Pacientes` ahora tiene `fechaNacimiento`, `foto` (ruta VARCHAR) y `diagnostico` 
- Añadida tabla `Administrador`
- Añadidas tablas `EvaluacionProfesional`, `Informe` y `Factura`
- Total de tablas: 14 → 17