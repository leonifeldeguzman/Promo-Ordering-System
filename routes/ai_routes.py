import os
import json
from flask import Blueprint, request, jsonify
from google import genai

# 1. Grab the API key from Railway's environment variables
api_key = os.environ.get("GEMINI_API_KEY")

# 2. Initialize your client ONCE seamlessly
client = genai.Client(api_key=api_key)

# 3. Create your blueprint route handler
ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')

# Your model tracking variable
MODEL_NAME = "gemini-2.5-flash-lite"


def get_menu_from_db():
    """Fetch current menu items from your PostgreSQL including images"""
    from database.db_connection import db_connection
    
    conn = db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT name, price, category, promo_details, image_url 
        FROM promos 
        WHERE status = 'Active' OR status = 'active'
    """)
    
    items = cur.fetchall()
    cur.close()
    conn.close()
    
    if not items:
        return "No menu items found. Please add items in admin panel."
    
    
    menu_text = "\n".join([
        f"- {item[0]}: ₱{float(item[1])} ({item[2]}) - Promo: {item[3] or 'None'} - Image: {item[4] or 'none'}" 
        for item in items
    ])
    return menu_text

@ai_bp.route('/recommend', methods=['POST'])
def recommend():
    """AI recommendation based on voice command (Multiple Items)"""
    try:
        data = request.json
        user_command = data.get('command', '')
        
        if not user_command:
            return jsonify({'error': 'No command provided'}), 400
            
        menu_items = get_menu_from_db()
        
        # Prompt changed to request a list/array of objects instead of just one item
        prompt = f"""
        You are SpeakNSave AI, a food recommendation assistant.
        Current menu:
        {menu_items}
        
        User voice command: "{user_command}"
        
        Suggest up to 3 distinct items that best match their request. 
        You MUST return valid JSON format matching this exact array structure:
        [
          {{"recommended_item": "item name", "price": price, "category": "category", "reason": "why this matches", "image_url": "filename or 'none'"}},
          ...
        ]
        If absolutely nothing matches, return an empty array [].
        """
        
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        
        clean_response = response.text.strip()
        if clean_response.startswith('```json'):
            clean_response = clean_response[7:-3]
        elif clean_response.startswith('```'):
            clean_response = clean_response[3:-3]
            
        result = json.loads(clean_response.strip())
        return jsonify(result)
        
    except Exception as e:
        print(f"AI Error: {e}")
        return jsonify([]), 200


@ai_bp.route('/suggest-promo', methods=['POST'])
def suggest_promo():
    """AI Promo suggestion based on craving/budget (Multiple Items)"""
    try:
        data = request.json
        craving = data.get('craving', '')
        budget = data.get('budget', None)
        
        menu_items = get_menu_from_db()
        
        # Prompt changed to request a list/array of promotional suggestions
        prompt = f"""
        Based on this menu:
        {menu_items}
        
        User budget: ₱{budget if budget else 'any'}
        User craving: {craving if craving else 'any'}
        
        Suggest up to 3 of the BEST value promos or meals that fit. Return valid JSON only as an array:
        [
          {{"suggestion": "item name", "price": price, "why": "reason why it is a great deal", "savings": "estimated savings", "image_url": "filename or 'none'"}},
          ...
        ]
        If nothing matches the criteria, return an empty array [].
        """
        
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        
        clean_response = response.text.strip()
        if clean_response.startswith('```json'):
            clean_response = clean_response[7:-3]
        elif clean_response.startswith('```'):
            clean_response = clean_response[3:-3]
            
        result = json.loads(clean_response.strip())
        return jsonify(result)
        
    except Exception as e:
        print(f"Promo AI Error: {e}")
        return jsonify([]), 200