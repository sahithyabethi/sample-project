{% extends 'base.html' %}

{% block content %}
<div class="auth-page">
    <div class="container" style="display: flex; justify-content: center; align-items: center;">
        <div class="form-card glass" style="margin: 0;">
            <h2 style="margin-bottom: 2rem; text-align: center;">Welcome Back</h2>
            <form method="post">
                {% csrf_token %}
                {% for field in form %}
                <div class="form-group">
                    <label>{{ field.label }}</label>
                    <input type="{{ field.field.widget.input_type }}" name="{{ field.name }}" class="form-control"
                        placeholder="{{ field.label }}">
                </div>
                {% endfor %}
                <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 1rem;">Login</button>
            </form>
            <p style="margin-top: 1.5rem; text-align: center; color: #ccc;">
                Don't have an account? <a href="{% url 'register' %}" style="color: var(--secondary-color);">Sign Up</a>
            </p>
        </div>
    </div>
</div>
{% endblock %}