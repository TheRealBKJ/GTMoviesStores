from django import template
register = template.Library()
@register.filter(name='get_quantity')
def get_cart_quantity(cart, movie_id):
    movie_id = str(movie_id)
    return cart.get(movie_id,0)