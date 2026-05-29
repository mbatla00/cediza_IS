# 🎨 GUÍA PARA PLANTILLAS HTML

## ¿Qué es esta carpeta?
Aquí van las vistas HTML renderizadas con **Jinja2** (motor de plantillas de Flask).
Usamos **Bootstrap 5** para el diseño responsive.

---

## 📐 PLANTILLA BASE (`base.html`) - YA CREADA

Todas las páginas heredan de `base.html`:

```html
{% extends "base.html" %}

{% block title %}Título de la página{% endblock %}

{% block content %}
    <!-- Contenido específico aquí -->
{% endblock %}

{% block extra_js %}
    <!-- JavaScript específico aquí (opcional) -->
{% endblock %}
```

## 🎯 ACCESO A DATOS DEL USUARIO

En cualquier plantilla podéis acceder a:

```html
{{ session.usuario_id }}
{{ session.usuario_nombre }}
{{ session.rol }}
```
## 📋 COMPONENTES DISPONIBLES (Bootstrap 5)

### Botones
```html
<a href="#" class="btn btn-primary btn-lg">Botón grande</a>
<button class="btn btn-success">Guardar</button>
```

### Tarjetas
```html
<div class="card shadow-sm">
    <div class="card-body">
        <h5 class="card-title">Título</h5>
        <p class="card-text">Contenido</p>
    </div>
</div>
```

### Formularios
```html
<form method="POST">
    <div class="mb-3">
        <label class="form-label">Nombre</label>
        <input type="text" name="nombre" class="form-control" required>
    </div>
    <button type="submit" class="btn btn-primary">Enviar</button>
</form>
```

### Alertas (mensajes flash)
Los mensajes flash aparecen automáticamente gracias a `base.html`.

## 📱 DISEÑO RESPONSIVE

- Usar clases `col-md-6 col-lg-4` para columnas adaptables
- Usar `btn-lg` y `fs-3` para botones grandes en móvil
- Las tablas deben ir dentro de `<div class="table-responsive">`

## 🎨 CLASES CSS PERSONALIZADAS (en style.css)

- `body.paciente-view` → Fuentes más grandes para pacientes mayores
- `.btn` → Mínimo 44x44px (estándar táctil Apple)