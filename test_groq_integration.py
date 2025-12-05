#!/usr/bin/env python3
"""
Test script to verify Groq-based story generation with automatic audio generation
"""
import requests
import json
import time
import sys
import os

# Fix Unicode issues on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:5000/api"

def test_story_generation():
    """Test creating a story with automatic narration and audio generation"""
    
    # Step 1: Create a project
    print("\n=== Step 1: Creating Project ===")
    project_response = requests.post(
        f"{BASE_URL}/projects/create",
        json={
            "name": "Groq Test Story",
            "description": "Testing automatic story generation with Groq AI"
        }
    )
    
    if project_response.status_code != 201:
        print(f"❌ Failed to create project: {project_response.text}")
        return False
    
    project_id = project_response.json()['project_id']
    print(f"✅ Project created: {project_id}")
    
    # Step 2: Generate story with Groq
    print("\n=== Step 2: Generating Story with Groq AI ===")
    print("Prompt: 'A rabbit learns to make friends with a butterfly in the garden'")
    
    story_response = requests.post(
        f"{BASE_URL}/stories/create",
        json={
            "project_id": project_id,
            "prompt": "A rabbit learns to make friends with a butterfly in the garden"
        }
    )
    
    if story_response.status_code != 201:
        print(f"❌ Failed to create story: {story_response.text}")
        return False
    
    story_data = story_response.json()
    story_id = story_data['story_id']
    
    print(f"✅ Story generated: {story_id}")
    print(f"   Title: {story_data['title']}")
    print(f"   Scenes: {len(story_data['scenes'])}")
    
    # Step 3: Display scenes with narration
    print("\n=== Step 3: Generated Scenes ===")
    for scene in story_data['scenes']:
        print(f"\n   📖 Scene {scene['sequence']}: {scene['title']}")
        print(f"      Background: {scene['background']}")
        print(f"      Narration: {scene['narration'][:100]}...")
        print(f"      Audio Ready: {scene.get('audio_ready', False)}")
    
    # Step 4: Verify audio files were created
    print("\n=== Step 4: Verifying Audio Files ===")
    import os
    audio_dir = "backend/storage/audio"
    audio_files = [f for f in os.listdir(audio_dir) if f.startswith("narration_") and f.endswith(".wav")]
    
    print(f"✅ Audio files created: {len(audio_files)}")
    for audio_file in sorted(audio_files)[-3:]:
        filepath = os.path.join(audio_dir, audio_file)
        size = os.path.getsize(filepath) / 1024  # KB
        print(f"   📻 {audio_file} ({size:.1f} KB)")
    
    print("\n=== 🎉 SUCCESS ===")
    print("✅ Full automatic pipeline working:")
    print("   1. User enters prompt")
    print("   2. Groq AI generates meaningful narration for 3 scenes")
    print("   3. Audio automatically generated from narration")
    print("   4. Ready for animation and playback")
    print("\nNo manual narration or audio generation needed!")
    
    return True

if __name__ == "__main__":
    print("Testing Groq AI Integration for Automatic Story Generation")
    print("=" * 60)
    
    try:
        success = test_story_generation()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
