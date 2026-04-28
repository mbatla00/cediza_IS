# 🏥 CEDIZA - Centro de Día Zamora 1

Aplicación web para la gestión integral de un centro de día: pacientes, trabajadores, cuestionarios cognitivos y generación de informes.

---

## 👥 EQUIPO

| Persona           | Rama                             | Responsabilidad |
|------------------|----------------------------------|-----------------|
| María    | `feature/arquitectura-seguridad` | Arquitectura, login, seguridad, protección de rutas, base visual |
| Sofía    | `feature/base-datos`             | Base de datos, modelos (VO), DAOs, scripts SQL |
| Alejandro    | `feature/paciente`               | Panel de paciente, cuestionarios, lógica de paciente |
| Mario | `feature/trabajador-admin`       | Panel trabajador/admin, gestión, informes |

---

## 🔐 AUTENTICACIÓN Y PERMISOS (MUY IMPORTANTE)

Responsabilidad **100% María**

Incluye:
- login / logout
- gestión de roles (paciente, trabajador, admin)
- protección de rutas
- control de acceso a vistas

👉 Es el sistema base de seguridad del proyecto.

---

## 📊 LÓGICA DE NEGOCIO

La lógica se divide para evitar duplicaciones:

- **Alejandro (Paciente)**
  - cuestionarios diarios
  - lógica de seguimiento del paciente
  - datos personales del paciente

- **Mario (Admin/Trabajador)**
  - generación de informes
  - gestión de usuarios
  - administración general del centro

⚠️ IMPORTANTE:
- No duplicar cálculos ni funciones entre módulos
- Si una lógica afecta a varios módulos → se centraliza y se discute antes

---

## 🎨 FRONTEND (VISTAS + DISEÑO)

El frontend es **compartido pero estructurado**, para evitar caos visual.

### 🧠 Filosofía del proyecto
- María define la base visual común
- Cada miembro implementa sus vistas usando esa base
- Todos respetan el mismo estilo

---

### 👥 REPARTO DE VISTAS

| Persona | Responsabilidad frontend |
|----------|------------------------|
| María | `base.html`, `login.html`, `style.css`, diseño general |
| Mario | `templates/paciente/*.html` |
| Alejandro | `templates/admin/*.html`, `templates/trabajador/*.html` |
| Sofía | Sin frontend (backend puro) |

---

### 🧱 REGLAS DE FRONTEND

- ✔️ Todas las páginas deben extender `base.html`
- ✔️ No romper el estilo global
- ✔️ CSS global solo lo modifica María
- ✔️ Cada módulo solo toca sus vistas
- ❌ No duplicar navbar, footer o layout
- ❌ No estilos distintos por módulo

---

## 🚀 CONFIGURACIÓN INICIAL

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TU-USUARIO/CEDIZA.git](https://github.com/TU-USUARIO/CEDIZA.git)
cd CEDIZA
```

### 2. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Variables de entorno
```bash
cp .env.example .env
```

### 5. Base de datos
```bash
mysql -u root -p db_cediza < sql/schema.sql
mysql -u root -p db_cediza < sql/inserts_test.sql
```

### 6. Ejecutar proyecto
```bash
python run.py
```

## 🌿 FLUJO DE TRABAJO CON GIT

### Crear rama
```bash
git checkout main
git pull origin main
git checkout -b feature/vuestra-parte
```

### Trabajo diario
```bash
git add .
git commit -m "Descripción clara"
git push
```

### Pull Request (OBLIGATORIO)
```bash
# 1. Subir rama
git push

# 2. Crear PR en GitHub
# base: main ← compare: feature/...

# 3. Asignar revisor (OTRO compañero)

# 4. Esperar aprobación

# 5. SOLO entonces hacer merge
```

## ⚠️ REGLAS

❌ No trabajar directamente en `main`  
❌ No hacer merge sin Pull Request  
❌ No aprobar tus propios PR  

✅ Usar siempre Pull Requests  
✅ Revisiones obligatorias por otro compañero  
✅ Pull desde `main` cada día  
✅ Commits claros y descriptivos  

---

## 📂 ESTRUCTURA

```text id="p7qk3m"
CEDIZA/
├── run.py
├── requirements.txt
├── .env.example
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   │
│   ├── models/
│   ├── dao/
│   ├── controllers/
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── admin/
│   │   ├── trabajador/
│   │   └── paciente/
│   │
│   └── static/
│       ├── css/
│       ├── js/
│       └── img/
│
├── sql/
└── docs/
