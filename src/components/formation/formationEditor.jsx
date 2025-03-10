import React, { useState, useEffect } from 'react';
import { DndProvider, useDrag, useDrop } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';

// Formation presets - positions for different formation types
const FORMATIONS = {
  '4-4-2': [
    { id: 'gk', name: 'Goalkeeper', x: 50, y: 90, playerId: null },
    { id: 'lb', name: 'Left Back', x: 20, y: 70, playerId: null },
    { id: 'cb1', name: 'Center Back (L)', x: 40, y: 70, playerId: null },
    { id: 'cb2', name: 'Center Back (R)', x: 60, y: 70, playerId: null },
    { id: 'rb', name: 'Right Back', x: 80, y: 70, playerId: null },
    { id: 'lm', name: 'Left Midfield', x: 20, y: 50, playerId: null },
    { id: 'cm1', name: 'Center Midfield (L)', x: 40, y: 50, playerId: null },
    { id: 'cm2', name: 'Center Midfield (R)', x: 60, y: 50, playerId: null },
    { id: 'rm', name: 'Right Midfield', x: 80, y: 50, playerId: null },
    { id: 'st1', name: 'Striker (L)', x: 40, y: 30, playerId: null },
    { id: 'st2', name: 'Striker (R)', x: 60, y: 30, playerId: null }
  ],
  '4-3-3': [
    { id: 'gk', name: 'Goalkeeper', x: 50, y: 90, playerId: null },
    { id: 'lb', name: 'Left Back', x: 20, y: 70, playerId: null },
    { id: 'cb1', name: 'Center Back (L)', x: 40, y: 70, playerId: null },
    { id: 'cb2', name: 'Center Back (R)', x: 60, y: 70, playerId: null },
    { id: 'rb', name: 'Right Back', x: 80, y: 70, playerId: null },
    { id: 'cdm', name: 'Defensive Midfield', x: 50, y: 50, playerId: null },
    { id: 'cm1', name: 'Center Midfield (L)', x: 35, y: 45, playerId: null },
    { id: 'cm2', name: 'Center Midfield (R)', x: 65, y: 45, playerId: null },
    { id: 'lw', name: 'Left Wing', x: 20, y: 25, playerId: null },
    { id: 'st', name: 'Striker', x: 50, y: 20, playerId: null },
    { id: 'rw', name: 'Right Wing', x: 80, y: 25, playerId: null }
  ],
  '3-5-2': [
    { id: 'gk', name: 'Goalkeeper', x: 50, y: 90, playerId: null },
    { id: 'cb1', name: 'Center Back (L)', x: 30, y: 70, playerId: null },
    { id: 'cb2', name: 'Center Back', x: 50, y: 70, playerId: null },
    { id: 'cb3', name: 'Center Back (R)', x: 70, y: 70, playerId: null },
    { id: 'lwb', name: 'Left Wing Back', x: 15, y: 55, playerId: null },
    { id: 'cm1', name: 'Center Midfield (L)', x: 35, y: 50, playerId: null },
    { id: 'cdm', name: 'Defensive Midfield', x: 50, y: 55, playerId: null },
    { id: 'cm2', name: 'Center Midfield (R)', x: 65, y: 50, playerId: null },
    { id: 'rwb', name: 'Right Wing Back', x: 85, y: 55, playerId: null },
    { id: 'st1', name: 'Striker (L)', x: 40, y: 30, playerId: null },
    { id: 'st2', name: 'Striker (R)', x: 60, y: 30, playerId: null }
  ],
  '5-3-2': [
    { id: 'gk', name: 'Goalkeeper', x: 50, y: 90, playerId: null },
    { id: 'lwb', name: 'Left Wing Back', x: 10, y: 70, playerId: null },
    { id: 'cb1', name: 'Center Back (L)', x: 30, y: 75, playerId: null },
    { id: 'cb2', name: 'Center Back', x: 50, y: 80, playerId: null },
    { id: 'cb3', name: 'Center Back (R)', x: 70, y: 75, playerId: null },
    { id: 'rwb', name: 'Right Wing Back', x: 90, y: 70, playerId: null },
    { id: 'cm1', name: 'Center Midfield (L)', x: 30, y: 50, playerId: null },
    { id: 'cm2', name: 'Center Midfield', x: 50, y: 50, playerId: null },
    { id: 'cm3', name: 'Center Midfield (R)', x: 70, y: 50, playerId: null },
    { id: 'st1', name: 'Striker (L)', x: 40, y: 30, playerId: null },
    { id: 'st2', name: 'Striker (R)', x: 60, y: 30, playerId: null }
  ],
  '4-5-1': [
    { id: 'gk', name: 'Goalkeeper', x: 50, y: 90, playerId: null },
    { id: 'lb', name: 'Left Back', x: 20, y: 70, playerId: null },
    { id: 'cb1', name: 'Center Back (L)', x: 40, y: 70, playerId: null },
    { id: 'cb2', name: 'Center Back (R)', x: 60, y: 70, playerId: null },
    { id: 'rb', name: 'Right Back', x: 80, y: 70, playerId: null },
    { id: 'lm', name: 'Left Midfield', x: 15, y: 50, playerId: null },
    { id: 'cm1', name: 'Center Midfield (L)', x: 35, y: 50, playerId: null },
    { id: 'cdm', name: 'Defensive Midfield', x: 50, y: 55, playerId: null },
    { id: 'cm2', name: 'Center Midfield (R)', x: 65, y: 50, playerId: null },
    { id: 'rm', name: 'Right Midfield', x: 85, y: 50, playerId: null },
    { id: 'st', name: 'Striker', x: 50, y: 30, playerId: null }
  ]
};

// Main Formation Editor Component
const FormationEditor = ({ 
  players = [], 
  onSave,
  initialFormation = null,
  teamId = null
}) => {
  // Initialize with 4-4-2 or provided formation
  const [formation, setFormation] = useState({
    name: '4-4-2',
    positions: [...FORMATIONS['4-4-2']]
  });
  
  const [availablePlayers, setAvailablePlayers] = useState([]);
  const [selectedPlayers, setSelectedPlayers] = useState([]);
  const [formationOptions] = useState(Object.keys(FORMATIONS));
  
  // Load initial formation if provided
  useEffect(() => {
    if (initialFormation) {
      setFormation(initialFormation);
      
      // Update selected/available players
      const selectedIds = initialFormation.positions
        .filter(pos => pos.playerId)
        .map(pos => pos.playerId);
        
      setSelectedPlayers(players.filter(p => selectedIds.includes(p.id)));
      setAvailablePlayers(players.filter(p => !selectedIds.includes(p.id)));
    } else {
      // No initial formation, all players are available
      setAvailablePlayers([...players]);
    }
  }, [initialFormation, players]);
  
  // Handle formation change
  const handleFormationChange = (e) => {
    const formationName = e.target.value;
    
    // Get new positions for the selected formation
    let newPositions = [...FORMATIONS[formationName]];
    
    // Preserve player assignments where possible by ID
    newPositions = newPositions.map(newPos => {
      const existingPos = formation.positions.find(p => p.id === newPos.id);
      return existingPos ? { ...newPos, playerId: existingPos.playerId } : newPos;
    });
    
    setFormation({ name: formationName, positions: newPositions });
  };
  
  // Handle player assignment to position
  const handleAssignPlayer = (positionId, playerId) => {
    // First, check if this player is already assigned elsewhere
    let playerToRemoveFromPosition = null;
    
    const updatedPositions = formation.positions.map(pos => {
      // If this is the position we're assigning to
      if (pos.id === positionId) {
        // Remember the player currently in this position (if any)
        if (pos.playerId) {
          playerToRemoveFromPosition = pos.playerId;
        }
        // Assign new player
        return { ...pos, playerId };
      }
      
      // If this position has the player we're moving, clear it
      if (pos.playerId === playerId) {
        return { ...pos, playerId: null };
      }
      
      return pos;
    });
    
    setFormation({ ...formation, positions: updatedPositions });
    
    // Update available and selected players lists
    const updatedSelected = [...selectedPlayers];
    const updatedAvailable = [...availablePlayers];
    
    // If we're assigning a new player to the position
    if (playerId) {
      // Find the player in either list
      const playerIndex = updatedAvailable.findIndex(p => p.id === playerId);
      
      if (playerIndex !== -1) {
        // Move from available to selected
        const player = updatedAvailable.splice(playerIndex, 1)[0];
        updatedSelected.push(player);
      }
    }
    
    // If we're removing a player from the position
    if (playerToRemoveFromPosition) {
      // Find the player in the selected list
      const playerIndex = updatedSelected.findIndex(p => p.id === playerToRemoveFromPosition);
      
      if (playerIndex !== -1) {
        // Move from selected to available
        const player = updatedSelected.splice(playerIndex, 1)[0];
        updatedAvailable.push(player);
      }
    }
    
    setSelectedPlayers(updatedSelected);
    setAvailablePlayers(updatedAvailable);
  };
  
  // Remove player from position
  const handleRemovePlayer = (positionId) => {
    const position = formation.positions.find(pos => pos.id === positionId);
    if (!position || !position.playerId) return;
    
    // Get player ID to remove
    const playerId = position.playerId;
    
    // Update formation positions
    const updatedPositions = formation.positions.map(pos => 
      pos.id === positionId ? { ...pos, playerId: null } : pos
    );
    
    setFormation({ ...formation, positions: updatedPositions });
    
    // Find player in selected list
    const playerIndex = selectedPlayers.findIndex(p => p.id === playerId);
    
    if (playerIndex !== -1) {
      // Move from selected to available
      const updatedSelected = [...selectedPlayers];
      const player = updatedSelected.splice(playerIndex, 1)[0];
      
      setSelectedPlayers(updatedSelected);
      setAvailablePlayers([...availablePlayers, player]);
    }
  };
  
  // Save the current formation
  const handleSaveFormation = () => {
    if (onSave) {
      const formationData = {
        ...formation,
        teamId
      };
      onSave(formationData);
    }
  };
  
  // Player Item component - for dragging
  const PlayerItem = ({ player }) => {
    const [{ isDragging }, dragRef] = useDrag({
      type: 'player',
      item: { id: player.id },
      collect: (monitor) => ({
        isDragging: monitor.isDragging(),
      }),
    });
    
    return (
      <div 
        ref={dragRef}
        className={`px-2 py-1 my-1 bg-white rounded border ${isDragging ? 'opacity-50' : ''} cursor-move flex items-center`}
      >
        <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center mr-2 text-xs font-bold">
          {player.number || '#'}
        </div>
        <div className="text-sm truncate">{player.name}</div>
      </div>
    );
  };
  
  // Position Drop Target component - on the pitch
  const PositionDropTarget = ({ position }) => {
    const player = position.playerId 
      ? selectedPlayers.find(p => p.id === position.playerId)
      : null;
      
    const [{ isOver }, dropRef] = useDrop({
      accept: 'player',
      drop: (item) => {
        handleAssignPlayer(position.id, item.id);
      },
      collect: (monitor) => ({
        isOver: monitor.isOver(),
      }),
    });
    
    return (
      <div 
        ref={dropRef}
        style={{ 
          left: `${position.x}%`, 
          top: `${position.y}%`,
          transform: 'translate(-50%, -50%)'
        }}
        className={`absolute w-16 h-16 rounded-full ${
          isOver ? 'bg-green-200' : player ? 'bg-green-500' : 'bg-gray-300'
        } flex flex-col items-center justify-center cursor-pointer shadow-md`}
        onClick={() => player && handleRemovePlayer(position.id)}
      >
        {player ? (
          <>
            <div className="text-white font-bold text-lg">{player.number || '#'}</div>
            <div className="text-white text-xs mt-1 max-w-full px-1 truncate">
              {player.name.split(' ')[0]}
            </div>
          </>
        ) : (
          <div className="text-xs text-center text-gray-700 px-1">{position.name}</div>
        )}
      </div>
    );
  };
  
  return (
    <DndProvider backend={HTML5Backend}>
      <div className="flex flex-col md:flex-row gap-4">
        {/* Formation controls */}
        <div className="w-full md:w-1/4">
          <div className="bg-white p-4 rounded shadow">
            <h3 className="text-lg font-bold mb-4">Formation Controls</h3>
            
            <div className="mb-4">
              <label className="block text-sm font-medium mb-1">Formation Type</label>
              <select 
                value={formation.name} 
                onChange={handleFormationChange}
                className="w-full p-2 border rounded"
              >
                {formationOptions.map(option => (
                  <option key={option} value={option}>{option}</option>
                ))}
              </select>
            </div>
            
            <button 
              onClick={handleSaveFormation}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
            >
              Save Formation
            </button>
          </div>
          
          {/* Available Players */}
          <div className="bg-white p-4 rounded shadow mt-4">
            <h3 className="text-lg font-bold mb-4">Available Players</h3>
            {availablePlayers.length === 0 ? (
              <p className="text-gray-500 text-sm">No available players</p>
            ) : (
              <div className="max-h-64 overflow-y-auto">
                {availablePlayers.map(player => (
                  <PlayerItem key={player.id} player={player} />
                ))}
              </div>
            )}
          </div>
        </div>
        
        {/* Pitch visualization */}
        <div className="w-full md:w-3/4">
          <div className="bg-green-700 rounded shadow relative" style={{ height: "600px" }}>
            {/* Field markings */}
            <div className="absolute inset-4 border-2 border-white rounded">
              {/* Center circle */}
              <div className="absolute left-1/2 top-1/2 w-32 h-32 border-2 border-white rounded-full" style={{ transform: 'translate(-50%, -50%)' }}></div>
              
              {/* Center line */}
              <div className="absolute left-0 right-0 top-1/2 h-0.5 bg-white"></div>
              
              {/* Penalty areas */}
              <div className="absolute bottom-0 left-1/2 w-64 h-32 border-2 border-white" style={{ transform: 'translate(-50%, 0)' }}></div>
              <div className="absolute top-0 left-1/2 w-64 h-32 border-2 border-white" style={{ transform: 'translate(-50%, 0)' }}></div>
              
              {/* Goal areas */}
              <div className="absolute bottom-0 left-1/2 w-32 h-12 border-2 border-white" style={{ transform: 'translate(-50%, 0)' }}></div>
              <div className="absolute top-0 left-1/2 w-32 h-12 border-2 border-white" style={{ transform: 'translate(-50%, 0)' }}></div>
            </div>
            
            {/* Player positions */}
            {formation.positions.map(position => (
              <PositionDropTarget key={position.id} position={position} />
            ))}
          </div>
        </div>
      </div>
    </DndProvider>
  );
};

export default FormationEditor;