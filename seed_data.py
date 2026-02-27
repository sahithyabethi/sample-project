{% extends 'base.html' %}

{% block content %}
<div class="container">
    <div class="glass"
        style="padding: 3rem; margin-top: 3rem; max-width: 900px; margin-left: auto; margin-right: auto;">
        <div style="display: flex; gap: 3rem; margin-bottom: 2rem; align-items: start;">
            {% if recipe.image %}
            <img src="{{ recipe.image.url }}"
                style="width: 300px; height: 300px; border-radius: 20px; object-fit: cover;">
            {% else %}
            <div
                style="width: 300px; height: 300px; background: #333; border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 5rem;">
                🍲</div>
            {% endif %}

            <div style="flex: 1;">
                <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">{{ recipe.name }}</h1>
                <p style="color: #ccc; margin-bottom: 1.5rem;">{{ recipe.description }}</p>
                <div style="display: flex; gap: 2rem;">
                    <div>
                        <h4 style="color: var(--secondary-color);">Prep Time</h4>
                        <p>{{ recipe.prep_time }} mins</p>
                    </div>
                </div>
            </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 3rem;">
            <div>
                <h3 style="margin-bottom: 1rem; border-bottom: 1px solid var(--glass-border); padding-bottom: 0.5rem;">
                    Ingredients</h3>
                <ul style="list-style: none;">
                    {% for ing in recipe.ingredients.all %}
                    <li
                        style="margin-bottom: 0.8rem; padding: 0.5rem; background: rgba(255,255,255,0.05); border-radius: 10px;">
                        <strong>{{ ing.quantity }}</strong> {{ ing.name }}
                    </li>
                    {% endfor %}
                </ul>
            </div>

            <div>
                <h3 style="margin-bottom: 1rem; border-bottom: 1px solid var(--glass-border); padding-bottom: 0.5rem;">
                    Cooking Steps</h3>
                <div style="line-height: 1.6; color: #eee; white-space: pre-line;">
                    {{ recipe.instructions }}
                </div>
            </div>
        </div>

        <div style="margin-top: 3rem; text-align: center;">
            <a href="{% url 'dashboard' %}" class="btn btn-secondary">Back to Dashboard</a>
        </div>
    </div>
</div>
{% endblock %}