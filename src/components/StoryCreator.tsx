'use client';

import { useState } from 'react';
import { api } from '@/lib/api';
import { Wand2 } from 'lucide-react';

export default function StoryCreator({ projectId, onStoryCreated }: { projectId: string; onStoryCreated?: () => void }) {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [story, setStory] = useState<any>(null);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const result = await api.createStory(projectId, prompt);
      setStory(result);
      // Callback to refresh project data
      if (onStoryCreated) {
        onStoryCreated();
      }
    } catch (error) {
      alert('Failed to generate story');
    }
    setLoading(false);
  };

  return (
    <div className="space-y-4">
      <form onSubmit={handleGenerate} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">Story Prompt</label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Describe your story... e.g., 'A brave little rabbit finds a magical forest'"
            rows={6}
          />
        </div>
        <button
          type="submit"
          disabled={loading || !prompt}
          className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center justify-center gap-2"
        >
          <Wand2 size={20} /> {loading ? 'Generating...' : 'Generate Story'}
        </button>
      </form>

      {story && (
        <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
          <h3 className="font-bold mb-2">{story.title}</h3>
          <div className="space-y-2">
            {story.scenes?.map((scene: any, idx: number) => (
              <div key={idx} className="text-sm text-gray-700">
                <strong>Scene {scene.sequence}:</strong> {scene.title}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
