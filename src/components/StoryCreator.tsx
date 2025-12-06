'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { Wand2, Play, Pause, Download, Sparkles, Volume2 } from 'lucide-react';

export default function StoryCreator({ projectId, onStoryCreated, generatedStory, onStoryGenerated }: { projectId: string; onStoryCreated?: () => void; generatedStory?: any; onStoryGenerated?: (story: any) => void }) {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [story, setStory] = useState<any>(generatedStory || null);
  const [playingAudio, setPlayingAudio] = useState<{[key: string]: boolean}>({});
  const [audioPlayer, setAudioPlayer] = useState<{[key: string]: HTMLAudioElement}>({});

  // Sync parent story state when it changes
  useEffect(() => {
    if (generatedStory) {
      setStory(generatedStory);
    }
  }, [generatedStory]);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const result = await api.createStory(projectId, prompt);
      setStory(result);
      // Persist story to parent state
      if (onStoryGenerated) {
        onStoryGenerated(result);
      }
      // Callback to refresh project data
      if (onStoryCreated) {
        onStoryCreated();
      }
    } catch (error) {
      alert('Failed to generate story');
    }
    setLoading(false);
  };

  const handlePlayPause = (sceneId: string, audioFilename: string) => {
    if (playingAudio[sceneId]) {
      // Pause
      const player = audioPlayer[sceneId];
      if (player) {
        player.pause();
      }
      setPlayingAudio({ ...playingAudio, [sceneId]: false });
    } else {
      // Play
      const audio = new Audio(`http://localhost:5000/api/audio/${audioFilename}`);
      audio.onended = () => {
        setPlayingAudio({ ...playingAudio, [sceneId]: false });
      };
      audio.play();
      setAudioPlayer({ ...audioPlayer, [sceneId]: audio });
      setPlayingAudio({ ...playingAudio, [sceneId]: true });
    }
  };

  const handleDownload = (audioFilename: string, sceneTitle: string) => {
    const link = document.createElement('a');
    link.href = `http://localhost:5000/api/audio/${audioFilename}`;
    link.download = `${sceneTitle}.wav`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-6">
      <form onSubmit={handleGenerate} className="space-y-4 bg-linear-to-br from-blue-50 to-purple-50 p-6 rounded-lg border-2 border-blue-200">
        <div>
          <label className="flex items-center gap-2 text-sm font-bold mb-3 text-gray-800">
            <Sparkles size={18} className="text-purple-600" />
            Story Prompt (AI-Powered)
          </label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            className="w-full px-4 py-3 border-2 border-blue-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent text-gray-800 placeholder-gray-500"
            placeholder="Describe your story... e.g., 'A brave little rabbit finds a magical forest' or 'Three friends go on an adventure to find treasure'"
            rows={5}
          />
        </div>
        <button
          type="submit"
          disabled={loading || !prompt}
          className="w-full bg-linear-to-r from-blue-600 to-purple-600 text-white py-3 rounded-lg hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 font-bold transition transform hover:scale-105"
        >
          <Wand2 size={20} /> {loading ? 'Creating Your Story...' : 'Generate Story with AI'}
        </button>
      </form>

      {story && (
        <div className="space-y-4">
          {/* Story Title */}
          <div className="bg-linear-to-r from-green-50 to-blue-50 rounded-lg p-6 border-2 border-green-300 shadow-md">
            <h2 className="text-2xl font-bold text-gray-800 mb-2 flex items-center gap-2">
              <Sparkles size={24} className="text-yellow-500" />
              {story.title}
            </h2>
            <p className="text-green-700 font-semibold flex items-center gap-2">
              ✅ Story Generated Successfully - Audio Ready!
            </p>
          </div>

          {/* Scenes Display */}
          <div className="grid grid-cols-1 gap-4">
            {story.scenes?.map((scene: any, idx: number) => {
              const audioFilename = scene.audio_filename || `narration_${scene.id}.wav`;
              return (
                <div key={idx} className="bg-white rounded-lg border-2 border-blue-200 overflow-hidden shadow-lg hover:shadow-xl transition">
                  {/* Scene Header */}
                  <div className="bg-linear-to-r from-blue-500 to-purple-500 text-white p-4">
                    <div className="font-bold text-lg">📺 Scene {scene.sequence}: {scene.title}</div>
                    <div className="text-blue-100 text-sm mt-1">Background: {scene.background}</div>
                  </div>

                  {/* Scene Content */}
                  <div className="p-5 space-y-4">
                    {/* Narration with Speech Bubble Style */}
                    <div className="bg-linear-to-r from-yellow-50 to-orange-50 rounded-lg p-4 border-l-4 border-yellow-400">
                      <div className="flex items-start gap-3">
                        <Volume2 size={20} className="text-orange-600 mt-1 shrink-0" />
                        <div>
                          <div className="font-semibold text-gray-700 mb-2">💬 Character Says:</div>
                          <div className="text-gray-800 leading-relaxed italic text-lg">
                            "{scene.narration}"
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Audio Controls */}
                    <div className="flex items-center gap-3 flex-wrap">
                      <button
                        onClick={() => handlePlayPause(scene.id, audioFilename)}
                        className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-bold transition transform hover:scale-105 ${
                          playingAudio[scene.id]
                            ? 'bg-red-500 text-white hover:bg-red-600 shadow-lg'
                            : 'bg-blue-500 text-white hover:bg-blue-600 shadow-md'
                        }`}
                      >
                        {playingAudio[scene.id] ? (
                          <>
                            <Pause size={16} /> Pause Narration
                          </>
                        ) : (
                          <>
                            <Play size={16} /> Play Narration
                          </>
                        )}
                      </button>
                      <button
                        onClick={() => handleDownload(audioFilename, scene.title)}
                        className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-bold bg-green-600 text-white hover:bg-green-700 transition transform hover:scale-105 shadow-md"
                      >
                        <Download size={16} /> Download Audio
                      </button>
                      <span className="text-xs text-gray-500 bg-gray-100 px-3 py-1 rounded-full">
                        🎵 Auto-Generated with TTS
                      </span>
                    </div>

                    {/* Character Info */}
                    <div className="bg-purple-50 rounded-lg p-3 border border-purple-200">
                      <div className="text-xs font-semibold text-purple-700 mb-2">👥 Characters & Setting:</div>
                      <div className="text-sm text-gray-700">
                        <span className="font-semibold">Location:</span> {scene.background}
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Info Box */}
          <div className="bg-blue-100 border-l-4 border-blue-500 p-4 rounded">
            <p className="text-sm text-blue-900 font-semibold mb-2">💡 Next Steps:</p>
            <ul className="text-sm text-blue-800 space-y-1 list-disc list-inside">
              <li>All narration has been automatically generated with AI text-to-speech</li>
              <li>Characters are set to animate and speak in sync with the audio</li>
              <li>Go to the "Edit" tab to customize character expressions and positions</li>
              <li>Visit the "Viewer" to see the full animated story with talking characters</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
