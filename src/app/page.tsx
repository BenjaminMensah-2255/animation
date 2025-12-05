import Link from 'next/link';
import { Play, Sparkles, FilmIcon } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2 text-2xl font-bold text-blue-600">
            <FilmIcon size={28} /> Cartoon Studio
          </div>
          <div className="flex gap-4">
            <Link href="/projects" className="text-gray-700 hover:text-blue-600">
              Projects
            </Link>
            <Link
              href="/projects/new"
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              Create
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="bg-linear-to-r from-blue-600 to-purple-600 text-white py-20">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-4 flex items-center justify-center gap-3">
            <Sparkles size={40} /> Create Animated Stories
          </h1>
          <p className="text-xl mb-8 text-blue-100">
            No design skills needed. Create children's-style animations in minutes.
          </p>
          <Link
            href="/projects/new"
            className="inline-flex bg-white text-blue-600 px-8 py-3 rounded-lg font-bold hover:bg-blue-50 items-center gap-2"
          >
            <Play size={20} /> Start Creating
          </Link>
        </div>
      </div>

      {/* Features */}
      <div className="max-w-6xl mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold mb-12 text-center">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-4xl mb-3">📖</div>
            <h3 className="font-bold text-lg mb-2">Write Your Story</h3>
            <p className="text-gray-600">
              Describe your story idea or use one of our templates to get started instantly.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-4xl mb-3">🎨</div>
            <h3 className="font-bold text-lg mb-2">Choose Characters & Scenes</h3>
            <p className="text-gray-600">
              Select from predefined characters and backgrounds, or customize them to your liking.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-4xl mb-3">🎬</div>
            <h3 className="font-bold text-lg mb-2">Generate & Export</h3>
            <p className="text-gray-600">
              Our engine animates your story with characters, transitions, and audio. Export as video.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-4xl mb-3">🎤</div>
            <h3 className="font-bold text-lg mb-2">Add Narration</h3>
            <p className="text-gray-600">
              Generate professional narration with text-to-speech. Narration syncs automatically.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-4xl mb-3">✏️</div>
            <h3 className="font-bold text-lg mb-2">Edit & Refine</h3>
            <p className="text-gray-600">
              Make adjustments to character positions, expressions, timing, and animations.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-4xl mb-3">💾</div>
            <h3 className="font-bold text-lg mb-2">Save & Share</h3>
            <p className="text-gray-600">
              Save your projects and regenerate whenever you want. Export as MP4 video.
            </p>
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="bg-blue-100 py-16">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Create?</h2>
          <p className="text-gray-700 mb-8">
            Start building your animated story today. No experience needed!
          </p>
          <Link
            href="/projects/new"
            className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg font-bold hover:bg-blue-700"
          >
            Create Your First Animation
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8">
        <div className="max-w-6xl mx-auto px-4 text-center text-gray-400">
          <p>&copy; 2025 Cartoon Animation Studio. Create amazing stories. No limits.</p>
        </div>
      </footer>
    </div>
  );
}
