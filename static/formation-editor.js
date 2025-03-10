/**
 * Formation Editor for ESMS
 * Allows visual editing of team formations
 */

// Positions for different formation types
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
  '4-2-3-1': [
    { id: 'gk', name: 'Goalkeeper', x: 50, y: 90, playerId: null },
    { id: 'lb', name: 'Left Back', x: 20, y: 70, playerId: null },
    { id: 'cb1', name: 'Center Back (L)', x: 40, y: 70, playerId: null },
    { id: 'cb2', name: 'Center Back (R)', x: 60, y: 70, playerId: null },
    { id: 'rb', name: 'Right Back', x: 80, y: 70, playerId: null },
    { id: 'dm1', name: 'Defensive Mid (L)', x: 40, y: 55, playerId: null },
    { id: 'dm2', name: 'Defensive Mid (R)', x: 60, y: 55, playerId: null },
    { id: 'lam', name: 'Left Attacking Mid', x: 30, y: 40, playerId: null },
    { id: 'cam', name: 'Center Attacking Mid', x: 50, y: 35, playerId: null },
    { id: 'ram', name: 'Right Attacking Mid', x: 70, y: 40, playerId: null },
    { id: 'st', name: 'Striker', x: 50, y: 20, playerId: null }
  ]
};

class FormationEditor {
  constructor(elementId) {
    this.container = document.getElementById(elementId);
    if (!this.container) {
      console.error('Container element not found!');
      return;
    }
    
    // Get data attributes
    this.teamId = this.container.getAttribute('data-team-id');
    this.apiUrl = this.container.getAttribute('data-api-url');
    this.saveUrl = this.container.getAttribute('data-save-url');
    
    // Initialize state
    this.players = [];
    this.availablePlayers = [];
    this.selectedPlayers = [];
    this.formation = {
      name: '4-4-2',
      positions: [...FORMATIONS['4-4-2']]
    };
    
    // Initialize the editor
    this.init();
  }
  
  async init() {
    // Clear the container first
    while (this.container.firstChild) {
      this.container.removeChild(this.container.firstChild);
    }
    
    // Create editor layout
    this.createLayout();
    
    // Load data
    await this.loadData();
    
    // Setup event handlers
    this.setupEventHandlers();
    
    // Initial render
    this.render();
  }
  
  createLayout() {
    this.container.innerHTML = `
      <div class="flex flex-col md:flex-row gap-4">
        <!-- Controls panel -->
        <div class="w-full md:w-1/4">
          <div class="bg-white p-4 rounded shadow">
            <h3 class="text-lg font-bold mb-4">Formation Controls</h3>
            
            <div class="mb-4">
              <label class="block text-sm font-medium mb-1">Formation Type</label>
              <select id="formation-select" class="w-full p-2 border rounded">
                ${Object.keys(FORMATIONS).map(formation => 
                  `<option value="${formation}">${formation}</option>`
                ).join('')}
              </select>
            </div>
            
            <button id="save-formation" class="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700">
              Save Formation
            </button>
            
            <div id="save-message" class="mt-2 text-center text-sm hidden"></div>
          </div>
          
          <!-- Available Players -->
          <div class="bg-white p-4 rounded shadow mt-4">
            <h3 class="text-lg font-bold mb-4">Available Players</h3>
            <div id="available-players" class="max-h-64 overflow-y-auto">
              <!-- Players will be added here -->
            </div>
          </div>
        </div>
        
        <!-- Pitch visualization -->
        <div class="w-full md:w-3/4">
          <div id="pitch" class="pitch rounded shadow">
            <!-- Field markings -->
            <div class="pitch-marking absolute inset-4 border rounded"></div>
            
            <!-- Center circle -->
            <div class="absolute left-1/2 top-1/2 w-32 h-32 border-2 border-white rounded-full" style="transform: translate(-50%, -50%)"></div>
            
            <!-- Center line -->
            <div class="absolute left-0 right-0 top-1/2 h-0.5 bg-white"></div>
            
            <!-- Penalty areas -->
            <div class="absolute bottom-0 left-1/2 w-64 h-32 border-2 border-white" style="transform: translate(-50%, 0)"></div>
            <div class="absolute top-0 left-1/2 w-64 h-32 border-2 border-white" style="transform: translate(-50%, 0)"></div>
            
            <!-- Goal areas -->
            <div class="absolute bottom-0 left-1/2 w-32 h-12 border-2 border-white" style="transform: translate(-50%, 0)"></div>
            <div class="absolute top-0 left-1/2 w-32 h-12 border-2 border-white" style="transform: translate(-50%, 0)"></div>
            
            <!-- Player positions will be added here -->
            <div id="positions-container"></div>
          </div>
        </div>
      </div>
    `;
  }
  
  async loadData() {
    try {
      // Get formation data from API
      const response = await fetch(this.apiUrl);
      const data = await response.json();
      
      // Update formation type
      this.formation.name = data.formation_type || '4-4-2';
      document.getElementById('formation-select').value = this.formation.name;
      
      // Load positions
      const positionsData = data.positions;
      this.formation.positions = [...FORMATIONS[this.formation.name]];
      
      // Apply saved player assignments
      if (positionsData) {
        for (const posId in positionsData) {
          const position = this.formation.positions.find(p => p.id === posId);
          if (position) {
            position.playerId = positionsData[posId];
          }
        }
      }
      
      // Get players data
      // In a real app, you'd fetch this from your API
      // For now, we'll create sample data
      this.players = await this.fetchPlayers();
      
      // Separate available and selected players
      this.updatePlayerLists();
      
    } catch (error) {
      console.error('Error loading formation data:', error);
      // Show error message
      const saveMessage = document.getElementById('save-message');
      saveMessage.textContent = 'Error loading data. Please try again.';
      saveMessage.classList.remove('hidden', 'text-green-500');
      saveMessage.classList.add('text-red-500');
      setTimeout(() => saveMessage.classList.add('hidden'), 3000);
    }
  }
  
  async fetchPlayers() {
    // In a real app, you'd fetch this from your API
    // For now we'll use placeholder data
    try {
      const response = await fetch(`/api/team/${this.teamId}/players`);
      return await response.json();
    } catch (error) {
      console.error('Error fetching players:', error);
      // Return sample data as fallback
      return [
        { id: 1, name: 'John Smith', position: 'GK', number: 1 },
        { id: 2, name: 'David Jones', position: 'CB', number: 2 },
        { id: 3, name: 'Michael Brown', position: 'CB', number: 3 },
        { id: 4, name: 'Robert Wilson', position: 'LB', number: 4 },
        { id: 5, name: 'James Taylor', position: 'RB', number: 5 },
        { id: 6, name: 'William Davis', position: 'CM', number: 6 },
        { id: 7, name: 'Richard Miller', position: 'CM', number: 7 },
        { id: 8, name: 'Joseph Allen', position: 'DM', number: 8 },
        { id: 9, name: 'Thomas Young', position: 'LM', number: 9 },
        { id: 10, name: 'Charles King', position: 'RM', number: 10 },
        { id: 11, name: 'Daniel Scott', position: 'ST', number: 11 },
        { id: 12, name: 'Matthew Green', position: 'ST', number: 12 },
        { id: 13, name: 'Anthony Baker', position: 'GK', number: 13 },
        { id: 14, name: 'Donald Nelson', position: 'CM', number: 14 },
        { id: 15, name: 'Mark Carter', position: 'ST', number: 15 }
      ];
    }
  }
  
  updatePlayerLists() {
    // Get all playerIds currently in positions
    const assignedPlayerIds = this.formation.positions
      .filter(pos => pos.playerId)
      .map(pos => pos.playerId);
    
    // Update available and selected lists
    this.availablePlayers = this.players.filter(p => !assignedPlayerIds.includes(p.id));
    this.selectedPlayers = this.players.filter(p => assignedPlayerIds.includes(p.id));
  }
  
  setupEventHandlers() {
    // Formation select change handler
    document.getElementById('formation-select').addEventListener('change', (e) => {
      this.changeFormation(e.target.value);
    });
    
    // Save button click handler
    document.getElementById('save-formation').addEventListener('click', () => {
      this.saveFormation();
    });
  }
  
  changeFormation(formationName) {
    if (!FORMATIONS[formationName]) {
      console.error(`Formation ${formationName} not found`);
      return;
    }
    
    // Save current player assignments
    const currentAssignments = {};
    this.formation.positions.forEach(pos => {
      if (pos.playerId) {
        currentAssignments[pos.id] = pos.playerId;
      }
    });
    
    // Update formation
    this.formation.name = formationName;
    this.formation.positions = [...FORMATIONS[formationName]];
    
    // Try to preserve player assignments where position IDs match
    this.formation.positions.forEach(pos => {
      if (currentAssignments[pos.id]) {
        pos.playerId = currentAssignments[pos.id];
      }
    });
    
    // Update player lists
    this.updatePlayerLists();
    
    // Re-render
    this.render();
  }
  
  async saveFormation() {
    // Prepare data for saving
    const positionsData = {};
    this.formation.positions.forEach(pos => {
      if (pos.playerId) {
        positionsData[pos.id] = pos.playerId;
      }
    });
    
    const formationData = {
      team_id: this.teamId,
      formation_type: this.formation.name,
      positions: positionsData
    };
    
    try {
      // Save to server
      const response = await fetch(this.saveUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formationData)
      });
      
      const result = await response.json();
      
      // Show success/error message
      const saveMessage = document.getElementById('save-message');
      if (result.success) {
        saveMessage.textContent = 'Formation saved successfully!';
        saveMessage.classList.remove('hidden', 'text-red-500');
        saveMessage.classList.add('text-green-500');
      } else {
        saveMessage.textContent = result.error || 'Error saving formation.';
        saveMessage.classList.remove('hidden', 'text-green-500');
        saveMessage.classList.add('text-red-500');
      }
      
      // Hide message after 3 seconds
      setTimeout(() => saveMessage.classList.add('hidden'), 3000);
      
    } catch (error) {
      console.error('Error saving formation:', error);
      
      // Show error message
      const saveMessage = document.getElementById('save-message');
      saveMessage.textContent = 'Error saving formation. Please try again.';
      saveMessage.classList.remove('hidden', 'text-green-500');
      saveMessage.classList.add('text-red-500');
      setTimeout(() => saveMessage.classList.add('hidden'), 3000);
    }
  }
  
  render() {
    // Render player positions
    this.renderPositions();
    
    // Render available players
    this.renderAvailablePlayers();
  }
  
  renderPositions() {
    const container = document.getElementById('positions-container');
    if (!container) return;
    
    // Clear existing positions
    container.innerHTML = '';
    
    // Add position elements
    this.formation.positions.forEach(position => {
      const player = position.playerId ? 
        this.players.find(p => p.id === position.playerId) : null;
      
      const positionEl = document.createElement('div');
      positionEl.className = `player-position ${player ? 'occupied' : ''}`;
      positionEl.style.left = `${position.x}%`;
      positionEl.style.top = `${position.y}%`;
      positionEl.setAttribute('data-position-id', position.id);
      
      if (player) {
        positionEl.innerHTML = `
          <div class="font-bold text-lg">${player.number || '#'}</div>
          <div class="text-xs mt-1 max-w-full px-1 truncate">
            ${player.name.split(' ')[0]}
          </div>
        `;
        
        // Click to remove player
        positionEl.addEventListener('click', () => {
          this.removePlayerFromPosition(position.id);
        });
      } else {
        positionEl.innerHTML = `
          <div class="text-xs text-center text-gray-700 px-1">${position.name}</div>
        `;
      }
      
      // Add dragover event listeners for drop target
      positionEl.addEventListener('dragover', (e) => {
        e.preventDefault();
        positionEl.classList.add('dragging-over');
      });
      
      positionEl.addEventListener('dragleave', () => {
        positionEl.classList.remove('dragging-over');
      });
      
      positionEl.addEventListener('drop', (e) => {
        e.preventDefault();
        positionEl.classList.remove('dragging-over');
        
        // Get the dragged player ID
        const playerId = e.dataTransfer.getData('player-id');
        if (playerId) {
          this.assignPlayerToPosition(parseInt(playerId), position.id);
        }
      });
      
      container.appendChild(positionEl);
    });
  }
  
  renderAvailablePlayers() {
    const container = document.getElementById('available-players');
    if (!container) return;
    
    // Clear container
    container.innerHTML = '';
    
    if (this.availablePlayers.length === 0) {
      container.innerHTML = '<p class="text-gray-500 text-sm">No available players</p>';
      return;
    }
    
    // Add player items
    this.availablePlayers.forEach(player => {
      const playerEl = document.createElement('div');
      playerEl.className = 'player-item';
      playerEl.setAttribute('draggable', 'true');
      playerEl.setAttribute('data-player-id', player.id);
      
      playerEl.innerHTML = `
        <div class="player-icon">${player.number || '#'}</div>
        <div class="text-sm truncate">${player.name} (${player.position})</div>
      `;
      
      // Setup drag events
      playerEl.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('player-id', player.id);
      });
      
      container.appendChild(playerEl);
    });
  }
  
  assignPlayerToPosition(playerId, positionId) {
    // Find the position
    const position = this.formation.positions.find(p => p.id === positionId);
    if (!position) return;
    
    // Find the player
    const player = this.players.find(p => p.id === playerId);
    if (!player) return;
    
    // If this position already has a player, make them available again
    if (position.playerId) {
      const currentPlayer = this.players.find(p => p.id === position.playerId);
      if (currentPlayer) {
        this.availablePlayers.push(currentPlayer);
      }
    }
    
    // If this player is already in another position, remove them
    const currentPosition = this.formation.positions.find(p => p.playerId === playerId);
    if (currentPosition) {
      currentPosition.playerId = null;
    }
    
    // Assign player to position
    position.playerId = playerId;
    
    // Update player lists
    this.updatePlayerLists();
    
    // Re-render
    this.render();
  }
  
  removePlayerFromPosition(positionId) {
    // Find the position
    const position = this.formation.positions.find(p => p.id === positionId);
    if (!position || !position.playerId) return;
    
    // Find the player
    const player = this.players.find(p => p.id === position.playerId);
    if (!player) return;
    
    // Remove assignment
    position.playerId = null;
    
    // Update player lists
    this.updatePlayerLists();
    
    // Re-render
    this.render();
  }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  const editorContainer = document.getElementById('formation-editor');
  if (editorContainer) {
    new FormationEditor('formation-editor');
  }
});