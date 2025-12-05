'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { api } from '@/lib/api';
import { Plus, Edit2, Trash2, Play } from 'lucide-react';

export default function ProjectsList() {
  const [projects, setProjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const result = await api.listProjects();
      setProjects(Array.isArray(result) ? result : []);
    } catch (error) {
      console.error('Failed to load projects:', error);
    }
    setLoading(false);
  };

  const handleDelete = async (projectId: string) => {
    if (confirm('Are you sure you want to delete this project?')) {
      try {
        await api.deleteProject(projectId);
        setProjects(projects.filter(p => p.id !== projectId));
      } catch (error) {
        alert('Failed to delete project');
      }
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center min-h-screen">Loading...</div>;
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold">My Projects</h1>
          <Link
            href="/projects/new"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 flex items-center gap-2"
          >
            <Plus size={20} /> New Project
          </Link>
        </div>

        {projects.length === 0 ? (
          <div className="text-center py-16">
            <p className="text-xl text-gray-600 mb-4">No projects yet</p>
            <Link
              href="/projects/new"
              className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
            >
              Create Your First Project
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((project) => (
              <div key={project.id} className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6">
                <h2 className="text-xl font-bold mb-2">{project.name}</h2>
                <p className="text-gray-600 mb-4 line-clamp-2">{project.description}</p>
                <div className="text-sm text-gray-500 mb-4">
                  {new Date(project.created_at).toLocaleDateString()}
                </div>
                <div className="flex gap-2">
                  <Link
                    href={`/editor/${project.id}`}
                    className="flex-1 bg-blue-600 text-white py-2 rounded hover:bg-blue-700 flex items-center justify-center gap-2"
                  >
                    <Edit2 size={16} /> Edit
                  </Link>
                  <Link
                    href={`/viewer`}
                    className="flex-1 bg-green-600 text-white py-2 rounded hover:bg-green-700 flex items-center justify-center gap-2"
                    title="View animation"
                  >
                    <Play size={16} /> View
                  </Link>
                  <button
                    onClick={() => handleDelete(project.id)}
                    className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 flex items-center gap-2"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
