from openai import OpenAI
import json
import jieba
import jieba.analyse
import re
from textblob import TextBlob
import emoji
import random
from typing import List, Dict, Tuple
import os

class ContentAdapter:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        self.post_patterns = {
            'intros': [
                '分享一下', '安利一下', '测评时间', '今日推荐', '好物分享',
                '终于找到了', '不得不分享', '这是我的必备', '一定要安利',
                '重磅推荐', '深度体验', '我的心得分享'
            ],
            'emojis': {
                'positive': ['✨', '💫', '🌟', '❤️', '💕', '🥰', '🎉', '✅', '💝', '🌈'],
                'negative': ['💔', '😢', '😭', '💭', '❌', '⚠️'],
                'neutral': ['💡', '📝', '🔍', '💭', '📌', '🎯', '💫']
            }
        }

    def process_content(self, english_text: str) -> Dict:
        # Get translation
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful translator who specializes in casual, trendy Chinese social media content."},
                {"role": "user", "content": f"Translate this to natural, conversational Chinese post content for Red/Rednote/xiaohongshu (小红书) and use internet buzzwords or Chinese slangs if they fit naturally: {english_text}"}
            ],
            temperature=0.3
        )
        translated_text = response.choices[0].message.content.strip()
        
        # Get styled version
        styling_prompt = """
        Transform this Chinese text into a Rednote (小红书) style post. Follow these rules:
        1. Start with emojis and a catchy opening based on the content
        2. Try to incorporate 1-2 popular Chinese internet slang and buzzwords if they fit naturally 
        3. Format the content with no more than 10 emojis
        4. End with relevant hashtags based on the content (at least 3)
        5. Make it enthusiastic and personal
        6. Add line breaks for readability
        """
        
        style_response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": styling_prompt},
                {"role": "user", "content": translated_text}
            ],
            temperature=0.3  # Increased from 0.3 to 0.5 for more creative variations
        )
        styled_text = style_response.choices[0].message.content.strip()
        
        return {
            "translated": translated_text,
            "Rednote trendy style": styled_text
        }

if __name__ == "__main__":
    adapter = ContentAdapter()
    english_text = input()
    if english_text.strip():
        result = adapter.process_content(english_text)
        print(json.dumps(result, ensure_ascii=False))
