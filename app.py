from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import json

app = Flask(__name__)
app.secret_key = 'fashionstore_secret_2024'

# ─── Sample Product Data ───────────────────────────────────────────────────────
PRODUCTS = [
    # ── MEN ──────────────────────────────────────────────────────────────────
    {"id": 1,  "name": "Urban Slim Fit Jeans",        "brand": "Levi's",     "price": 1499, "original_price": 2999, "category": "men",   "sub": "jeans",   "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&q=80", "rating": 4.3, "reviews": 2340, "sizes": ["28","30","32","34","36"], "colors": ["Blue","Black","Grey"], "badge": "BESTSELLER"},
    {"id": 3,  "name": "Classic White Oxford Shirt",  "brand": "H&M",        "price": 899,  "original_price": 1599, "category": "men",   "sub": "shirts",  "image": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=400&q=80", "rating": 4.1, "reviews": 980,  "sizes": ["S","M","L","XL","XXL"], "colors": ["White","Blue","Pink"], "badge": ""},
    {"id": 5,  "name": "Cargo Jogger Pants",          "brand": "Nike",       "price": 2199, "original_price": 3499, "category": "men",   "sub": "pants",   "image": "https://images.unsplash.com/photo-1607522370275-f14206abe5d3?w=400&q=80", "rating": 4.6, "reviews": 3210, "sizes": ["S","M","L","XL","XXL"], "colors": ["Black","Khaki","Grey"], "badge": "HOT"},
    {"id": 7,  "name": "Oversized Graphic Tee",       "brand": "H&M",        "price": 599,  "original_price": 999,  "category": "men",   "sub": "tshirts", "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&q=80", "rating": 4.0, "reviews": 560,  "sizes": ["S","M","L","XL","XXL"], "colors": ["White","Black","Red"], "badge": ""},
    {"id": 9,  "name": "Leather Biker Jacket",        "brand": "Roadster",   "price": 3499, "original_price": 5999, "category": "men",   "sub": "jackets", "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&q=80", "rating": 4.7, "reviews": 2100, "sizes": ["S","M","L","XL","XXL"], "colors": ["Black","Brown"], "badge": "BESTSELLER"},
    {"id": 11, "name": "Denim Trucker Jacket",        "brand": "Levi's",     "price": 2799, "original_price": 4499, "category": "men",   "sub": "jackets", "image": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400&q=80", "rating": 4.5, "reviews": 1760, "sizes": ["S","M","L","XL","XXL"], "colors": ["Blue","Black"], "badge": "TRENDING"},
    {"id": 13, "name": "Striped Polo T-Shirt",        "brand": "U.S. Polo",  "price": 799,  "original_price": 1399, "category": "men",   "sub": "tshirts", "image": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400&q=80", "rating": 4.2, "reviews": 1120, "sizes": ["S","M","L","XL","XXL"], "colors": ["Navy","White","Red"], "badge": ""},
    {"id": 14, "name": "Formal Slim Fit Trousers",    "brand": "Raymond",    "price": 1899, "original_price": 2999, "category": "men",   "sub": "pants",   "image": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=400&q=80", "rating": 4.3, "reviews": 870,  "sizes": ["28","30","32","34","36"], "colors": ["Black","Navy","Grey"], "badge": ""},
    {"id": 15, "name": "Linen Summer Shirt",          "brand": "FabIndia",   "price": 1199, "original_price": 1999, "category": "men",   "sub": "shirts",  "image": "https://images.unsplash.com/photo-1620012253295-c15cc3e65df4?w=400&q=80", "rating": 4.4, "reviews": 640,  "sizes": ["S","M","L","XL","XXL"], "colors": ["Beige","White","Blue"], "badge": "NEW"},
    {"id": 16, "name": "Athletic Running Shorts",     "brand": "Adidas",     "price": 999,  "original_price": 1799, "category": "men",   "sub": "pants",   "image": "https://images.unsplash.com/photo-1562886877-4b3e3f74e8b5?w=400&q=80", "rating": 4.5, "reviews": 2200, "sizes": ["S","M","L","XL","XXL"], "colors": ["Black","Grey","Blue"], "badge": "HOT"},

    # ── WOMEN ─────────────────────────────────────────────────────────────────
    {"id": 2,  "name": "Floral Wrap Dress",           "brand": "Zara",       "price": 1299, "original_price": 2499, "category": "women", "sub": "dresses", "image": "https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=400&q=80", "rating": 4.5, "reviews": 1820, "sizes": ["XS","S","M","L","XL"], "colors": ["Pink","Blue","Green"], "badge": "NEW"},
    {"id": 4,  "name": "Boho Maxi Skirt",             "brand": "FabIndia",   "price": 1099, "original_price": 1999, "category": "women", "sub": "skirts",  "image": "https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=400&q=80", "rating": 4.4, "reviews": 650,  "sizes": ["XS","S","M","L","XL"], "colors": ["Orange","Red","Yellow"], "badge": "TRENDING"},
    {"id": 6,  "name": "Embroidered Kurti",           "brand": "Biba",       "price": 849,  "original_price": 1499, "category": "women", "sub": "kurtis",  "image": "https://images.unsplash.com/photo-1594938298603-c8148c4b4f35?w=400&q=80", "rating": 4.2, "reviews": 1450, "sizes": ["XS","S","M","L","XL"], "colors": ["Teal","Purple","Red"], "badge": ""},
    {"id": 8,  "name": "Off-Shoulder Crop Top",       "brand": "Zara",       "price": 699,  "original_price": 1299, "category": "women", "sub": "tops",    "image": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=400&q=80", "rating": 4.3, "reviews": 890,  "sizes": ["XS","S","M","L"], "colors": ["White","Black","Pink"], "badge": "NEW"},
    {"id": 10, "name": "Pleated Palazzo Pants",       "brand": "W",          "price": 1199, "original_price": 1999, "category": "women", "sub": "pants",   "image": "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=400&q=80", "rating": 4.1, "reviews": 430,  "sizes": ["XS","S","M","L","XL"], "colors": ["Black","White","Navy"], "badge": ""},
    {"id": 12, "name": "Silk Satin Midi Dress",       "brand": "Mango",      "price": 2499, "original_price": 4299, "category": "women", "sub": "dresses", "image": "https://images.unsplash.com/photo-1539008835657-9e8e9680c956?w=400&q=80", "rating": 4.6, "reviews": 980,  "sizes": ["XS","S","M","L"], "colors": ["Cream","Rose","Black"], "badge": "LUXURY"},
    {"id": 17, "name": "Printed Anarkali Kurta",      "brand": "Libas",      "price": 1399, "original_price": 2299, "category": "women", "sub": "kurtis",  "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=400&q=80", "rating": 4.4, "reviews": 1200, "sizes": ["XS","S","M","L","XL"], "colors": ["Pink","Yellow","Green"], "badge": "BESTSELLER"},
    {"id": 18, "name": "Denim Mini Skirt",            "brand": "H&M",        "price": 899,  "original_price": 1599, "category": "women", "sub": "skirts",  "image": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400&q=80", "rating": 4.0, "reviews": 540,  "sizes": ["XS","S","M","L"], "colors": ["Blue","Black","White"], "badge": ""},
    {"id": 19, "name": "Ribbed Bodycon Dress",        "brand": "Mango",      "price": 1799, "original_price": 2999, "category": "women", "sub": "dresses", "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&q=80", "rating": 4.5, "reviews": 760,  "sizes": ["XS","S","M","L"], "colors": ["Black","Camel","Red"], "badge": "TRENDING"},
    {"id": 20, "name": "Cotton Straight Kurti",       "brand": "Jaipur Kurti","price": 699, "original_price": 1199, "category": "women", "sub": "kurtis",  "image": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?w=400&q=80", "rating": 4.3, "reviews": 980,  "sizes": ["XS","S","M","L","XL"], "colors": ["Blue","White","Green"], "badge": ""},

    # ── KIDS ──────────────────────────────────────────────────────────────────
    {"id": 21, "name": "Dino Print T-Shirt",          "brand": "H&M Kids",   "price": 399,  "original_price": 699,  "category": "kids",  "sub": "tshirts", "image": "https://images.unsplash.com/photo-1622290291468-a28f7a7dc6a8?w=400&q=80", "rating": 4.6, "reviews": 890,  "sizes": ["2Y","4Y","6Y","8Y","10Y"], "colors": ["White","Yellow","Blue"], "badge": "BESTSELLER"},
    {"id": 22, "name": "Floral Frock",                "brand": "FirstCry",   "price": 599,  "original_price": 999,  "category": "kids",  "sub": "dresses", "image": "https://images.unsplash.com/photo-1471286174890-9c112ffca5b4?w=400&q=80", "rating": 4.7, "reviews": 1100, "sizes": ["2Y","4Y","6Y","8Y","10Y"], "colors": ["Pink","Purple","Yellow"], "badge": "NEW"},
    {"id": 23, "name": "Kids Denim Jeans",            "brand": "Levi's Kids","price": 999,  "original_price": 1799, "category": "kids",  "sub": "jeans",   "image": "https://images.unsplash.com/photo-1519457431-44ccd64a579b?w=400&q=80", "rating": 4.4, "reviews": 670,  "sizes": ["4Y","6Y","8Y","10Y","12Y"], "colors": ["Blue","Black"], "badge": ""},
    {"id": 24, "name": "Cartoon Hoodie",              "brand": "Zara Kids",  "price": 899,  "original_price": 1499, "category": "kids",  "sub": "jackets", "image": "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400&q=80", "rating": 4.5, "reviews": 520,  "sizes": ["4Y","6Y","8Y","10Y","12Y"], "colors": ["Red","Blue","Green"], "badge": "TRENDING"},
    {"id": 25, "name": "Ethnic Kurta Set",            "brand": "Fabindia Kids","price": 799, "original_price": 1299, "category": "kids",  "sub": "ethnic",  "image": "https://images.unsplash.com/photo-1604917621956-10dfa7cce2e7?w=400&q=80", "rating": 4.3, "reviews": 410,  "sizes": ["2Y","4Y","6Y","8Y","10Y"], "colors": ["Gold","Blue","Green"], "badge": ""},
    {"id": 26, "name": "Rainbow Striped Dress",       "brand": "Mothercare", "price": 699,  "original_price": 1199, "category": "kids",  "sub": "dresses", "image": "https://images.unsplash.com/photo-1518831959646-742c3a14ebf6?w=400&q=80", "rating": 4.6, "reviews": 830,  "sizes": ["2Y","4Y","6Y","8Y"], "colors": ["Multicolor"], "badge": "HOT"},
    {"id": 27, "name": "Boys Cargo Shorts",           "brand": "Nike Kids",  "price": 599,  "original_price": 999,  "category": "kids",  "sub": "shorts",  "image": "https://images.unsplash.com/photo-1565084888279-aca607ecce0c?w=400&q=80", "rating": 4.2, "reviews": 360,  "sizes": ["4Y","6Y","8Y","10Y","12Y"], "colors": ["Black","Grey","Khaki"], "badge": ""},
    {"id": 28, "name": "Unicorn Sweatshirt",          "brand": "H&M Kids",   "price": 799,  "original_price": 1399, "category": "kids",  "sub": "tshirts", "image": "https://images.unsplash.com/photo-1543269664-56d93c1b41a6?w=400&q=80", "rating": 4.8, "reviews": 1450, "sizes": ["4Y","6Y","8Y","10Y","12Y"], "colors": ["Pink","Lilac","White"], "badge": "BESTSELLER"},
    {"id": 29, "name": "Boys Formal Shirt + Pant",    "brand": "Allen Solly Junior","price": 1299, "original_price": 2199, "category": "kids", "sub": "ethnic", "image": "https://images.unsplash.com/photo-1604537529428-15bcbeecfe4d?w=400&q=80", "rating": 4.5, "reviews": 290,  "sizes": ["4Y","6Y","8Y","10Y","12Y"], "colors": ["White+Navy","White+Black"], "badge": "NEW"},
    {"id": 30, "name": "Girls Leggings (Pack of 3)",  "brand": "Mothercare", "price": 499,  "original_price": 899,  "category": "kids",  "sub": "pants",   "image": "https://images.unsplash.com/photo-1518831959646-742c3a14ebf6?w=400&q=80", "rating": 4.4, "reviews": 720,  "sizes": ["2Y","4Y","6Y","8Y","10Y"], "colors": ["Black","Pink","Grey"], "badge": ""},
]

def get_cart():
    return session.get('cart', {})

def save_cart(cart):
    session['cart'] = cart
    session.modified = True

def cart_count():
    cart = get_cart()
    return sum(item['qty'] for item in cart.values())

def cart_total():
    cart = get_cart()
    total = 0
    for key, item in cart.items():
        pid = int(key.split('_')[0])
        product = next((p for p in PRODUCTS if p['id'] == pid), None)
        if product:
            total += product['price'] * item['qty']
    return total

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    featured = PRODUCTS[:8]
    return render_template('index.html', products=featured,
                           cart_count=cart_count(), cart_total=cart_total())

@app.route('/products')
def products():
    category = request.args.get('category', 'all')
    sub = request.args.get('sub', '')
    sort = request.args.get('sort', 'popular')
    search = request.args.get('q', '').lower()

    filtered = PRODUCTS
    if category != 'all':
        filtered = [p for p in filtered if p['category'] == category]
    if sub:
        filtered = [p for p in filtered if p['sub'] == sub]
    if search:
        filtered = [p for p in filtered if search in p['name'].lower() or search in p['brand'].lower()]

    if sort == 'price_low':
        filtered.sort(key=lambda x: x['price'])
    elif sort == 'price_high':
        filtered.sort(key=lambda x: x['price'], reverse=True)
    elif sort == 'rating':
        filtered.sort(key=lambda x: x['rating'], reverse=True)
    elif sort == 'discount':
        filtered.sort(key=lambda x: x['original_price'] - x['price'], reverse=True)

    return render_template('products.html', products=filtered, category=category,
                           sub=sub, sort=sort, search=search,
                           cart_count=cart_count(), cart_total=cart_total())

@app.route('/product/<int:pid>')
def product_detail(pid):
    product = next((p for p in PRODUCTS if p['id'] == pid), None)
    if not product:
        flash('Product not found!', 'error')
        return redirect(url_for('products'))
    related = [p for p in PRODUCTS if p['category'] == product['category'] and p['id'] != pid][:4]
    return render_template('product_detail.html', product=product, related=related,
                           cart_count=cart_count(), cart_total=cart_total())

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    pid = int(request.form.get('product_id'))
    size = request.form.get('size', 'M')
    qty = int(request.form.get('qty', 1))
    key = f"{pid}_{size}"

    cart = get_cart()
    if key in cart:
        cart[key]['qty'] += qty
    else:
        cart[key] = {'pid': pid, 'size': size, 'qty': qty}
    save_cart(cart)
    flash('Item added to cart! 🛍️', 'success')

    next_page = request.form.get('next', url_for('cart'))
    if next_page == 'stay':
        return redirect(url_for('product_detail', pid=pid))
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<key>')
def remove_from_cart(key):
    cart = get_cart()
    if key in cart:
        del cart[key]
        save_cart(cart)
        flash('Item removed from cart.', 'info')
    return redirect(url_for('cart'))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    key = request.form.get('key')
    qty = int(request.form.get('qty', 1))
    cart = get_cart()
    if key in cart:
        if qty <= 0:
            del cart[key]
        else:
            cart[key]['qty'] = qty
        save_cart(cart)
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart = get_cart()
    cart_items = []
    subtotal = 0
    for key, item in cart.items():
        pid = item['pid']
        product = next((p for p in PRODUCTS if p['id'] == pid), None)
        if product:
            line_total = product['price'] * item['qty']
            subtotal += line_total
            cart_items.append({
                'key': key, 'product': product,
                'size': item['size'], 'qty': item['qty'],
                'line_total': line_total
            })
    discount = int(subtotal * 0.05) if subtotal > 1999 else 0
    delivery = 0 if subtotal >= 999 else 79
    total = subtotal - discount + delivery
    return render_template('cart.html', cart_items=cart_items, subtotal=subtotal,
                           discount=discount, delivery=delivery, total=total,
                           cart_count=cart_count(), cart_total=cart_total())

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if not get_cart():
        flash('Your cart is empty!', 'error')
        return redirect(url_for('products'))
    if request.method == 'POST':
        # Simulate order placement
        session['cart'] = {}
        session.modified = True
        flash('🎉 Order placed successfully! Track it in My Orders.', 'success')
        return redirect(url_for('order_success'))
    cart = get_cart()
    subtotal = cart_total()
    discount = int(subtotal * 0.05) if subtotal > 1999 else 0
    delivery = 0 if subtotal >= 999 else 79
    total = subtotal - discount + delivery
    return render_template('checkout.html', subtotal=subtotal, discount=discount,
                           delivery=delivery, total=total,
                           cart_count=cart_count(), cart_total=cart_total())

@app.route('/order-success')
def order_success():
    import random, string
    order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return render_template('order_success.html', order_id=order_id, cart_count=0)

@app.route('/wishlist')
def wishlist():
    wishlist_ids = session.get('wishlist', [])
    wished = [p for p in PRODUCTS if p['id'] in wishlist_ids]
    return render_template('wishlist.html', products=wished,
                           cart_count=cart_count(), cart_total=cart_total())

@app.route('/toggle_wishlist/<int:pid>')
def toggle_wishlist(pid):
    wl = session.get('wishlist', [])
    if pid in wl:
        wl.remove(pid)
        flash('Removed from wishlist', 'info')
    else:
        wl.append(pid)
        flash('Added to wishlist ❤️', 'success')
    session['wishlist'] = wl
    session.modified = True
    return redirect(request.referrer or url_for('products'))

@app.context_processor
def inject_globals():
    return dict(wishlist_ids=session.get('wishlist', []))

if __name__ == '__main__':
    app.run(debug=True)
