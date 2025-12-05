'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';

export default function CharacterSelector({ scene, onUpdate }: { scene: any; onUpdate: (s: any) => void }) {
  const [characters, setCharacters] = useState<any>({});
  const [selectedCharacters, setSelectedCharacters] = useState<string[]>([]);

  useEffect(() => {
    loadCharacters();
  }, []);

  const loadCharacters = async () => {
    try {
      const result = await api.getCharacters();
      setCharacters(result);
    } catch (error) {
      console.error('Failed to load characters:', error);
    }
  };

  const handleAddCharacter = (charId: string) => {
    const newCharacters = [
      ...(scene.characters || []),
      {
        character_id: charId,
        position: { x: 0.5, y: 0.7 },
        expression: 'neutral'
      }
    ];
    onUpdate({ ...scene, characters: newCharacters });
  };

  const handleUpdateCharacter = (idx: number, updates: any) => {
    const updated = [...(scene.characters || [])];
    updated[idx] = { ...updated[idx], ...updates };
    onUpdate({ ...scene, characters: updated });
  };

  const handleRemoveCharacter = (idx: number) => {
    const updated = [...(scene.characters || [])].filter((_, i) => i !== idx);
    onUpdate({ ...scene, characters: updated });
  };

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-2">Add Character</label>
        <div className="flex gap-2 flex-wrap">
          {Object.entries(characters).map(([key, char]: [string, any]) => (
            <button
              key={key}
              onClick={() => handleAddCharacter(key)}
              className="px-3 py-1 bg-blue-200 rounded hover:bg-blue-300 text-sm"
            >
              + {char.name}
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-3 border-t pt-4">
        {(scene.characters || []).map((char: any, idx: number) => {
          const charDef = characters[char.character_id];
          return (
            <div key={idx} className="bg-gray-100 p-3 rounded">
              <div className="flex justify-between items-start mb-2">
                <h4 className="font-medium">{charDef?.name || char.character_id}</h4>
                <button
                  onClick={() => handleRemoveCharacter(idx)}
                  className="text-red-600 text-sm hover:underline"
                >
                  Remove
                </button>
              </div>

              <div className="grid grid-cols-2 gap-2 text-sm">
                <div>
                  <label className="block text-xs mb-1">Expression</label>
                  <select
                    value={char.expression}
                    onChange={(e) => handleUpdateCharacter(idx, { expression: e.target.value })}
                    className="w-full px-2 py-1 border rounded text-xs"
                  >
                    {charDef?.expressions?.map((exp: string) => (
                      <option key={exp} value={exp}>
                        {exp}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-xs mb-1">X Position</label>
                  <input
                    type="number"
                    value={char.position?.x || 0.5}
                    onChange={(e) =>
                      handleUpdateCharacter(idx, {
                        position: { ...char.position, x: parseFloat(e.target.value) }
                      })
                    }
                    className="w-full px-2 py-1 border rounded text-xs"
                    min="0"
                    max="1"
                    step="0.1"
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
