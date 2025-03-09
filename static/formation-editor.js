/**
 * Formation Editor for ESMS
 * Interactive canvas for positioning players on a football pitch
 */

const formationEditor = {
    canvas: null,
    ctx: null,
    players: [],
    selectedPlayer: null,
    isDragging: false,
    fieldWidth: 600,
    fieldHeight: 400,
    teamId: null,
    
    // Formation templates with player positions (x, y as percentages of field)
    formations: {
        '4-4-2': [
            { position: 'GK', x: 0.06, y: 0.5 },
            { position: 'LB', x: 0.2, y: 0.2 },
            { position: 'CB', x: 0.2, y: 0.4 },
            { position: 'CB', x: 0.2, y: 0.6 },
            { position: 'RB', x: 0.2, y: 0.8 },
            { position: 'LM', x: 0.4, y: 0.2 },
            { position: 'CM', x: 0.4, y: 0.4 },
            { position: 'CM', x: 0.4, y: 0.6 },
            { position: 'RM', x: 0.4, y: 0.8 },
            { position: 'ST', x: 0.6, y: 0.4 },
            { position: 'ST', x: 0.6, y: 0.6 }
        ],
        '4-3-3': [
            { position: 'GK', x: 0.06, y: 0.5 },
            { position: 'LB', x: 0.2, y: 0.2 },
            { position: 'CB', x: 0.2, y: 0.4 },
            { position: 'CB', x: 0.2, y: 0.6 },
            { position: 'RB', x: 0.2, y: 0.8 },
            { position: 'CM', x: 0.4, y: 0.3 },
            { position: 'CM', x: 0.4, y: 0.5 },
            { position: 'CM', x: 0.4, y: 0.7 },
            { position: 'LW', x: 0.6, y: 0.2 },
            { position: 'ST', x: 0.6, y: 0.5 },
            { position: 'RW', x: 0.6, y: 0.8 }
        ],
        '3-5-2': [
            { position: 'GK', x: 0.06, y: 0.5 },
            { position: 'CB', x: 0.2, y: 0.3 },
            { position: 'CB', x: 0.2, y: 0.5 },
            { position: 'CB', x: 0.2, y: 0.7 },
            { position: 'LWB', x: 0.35, y: 0.1 },
            { position: 'CM', x: 0.4, y: 0.3 },
            { position: 'CM', x: 0.4, y: 0.5 },
            { position: 'CM', x: 0.4, y: 0.7 },
            { position: 'RWB', x: 0.35, y: 0.9 },
            { position: 'ST', x: 0.6, y: 0.4 },
            { position: 'ST', x: 0.6, y: 0.6 }
        ],
        '5-3-2': [
            { position: 'GK', x: 0.06, y: 0.5 },
            { position: 'LWB', x: 0.2, y: 0.1 },
            { position: 'CB', x: 0.2, y: 0.3 },
            { position: 'CB', x: 0.2, y: 0.5 },
            { position: 'CB', x: 0.2, y: 0.7 },
            { position: 'RWB', x: 0.2, y: 0.9 },
            { position: 'CM', x: 0.4, y: 0.3 },
            { position: 'CM', x: 0.4, y: 0.5 },
            { position: 'CM', x: 0.4, y: 0.7 },
            { position: 'ST', x: 0.6, y: 0.4 },
            { position: 'ST', x: 0.6, y: 0.6 }
        ],
        '4-2-3-1': [
            { position: 'GK', x: 0.06, y: 0.5 },
            { position: 'LB', x: 0.2, y: 0.2 },
            { position: 'CB', x: 0.2, y: 0.4 },
            { position: 'CB', x: 0.2, y: 0.6 },
            { position: 'RB', x: 0.2, y: 0.8 },
            { position: 'DM', x: 0.35, y: 0.35 },
            { position: 'DM', x: 0.35, y: 0.65 },
            { position: 'LW', x: 0.5, y: 0.2 },
            { position: 'AM', x: 0.5, y: 0.5 },
            { position: 'RW', x: 0.5, y: 0.8 },
            { position: 'ST', x: 0.65, y: 0.5 }
        ]
    },
    
    initialize(canvasId, teamId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) {
            console.error('Canvas element not found!');
            return;
        }
        
        this.ctx = this.canvas.getContext('2d');
        this.teamId = teamId;
        
        // Load team data
        this.loadTeamData();
        
        // Enable interaction
        this.setupEventListeners();
        
        // Formation selector
        const formationSelect = document.getElementById('formation');
        if (formationSelect) {
            formationSelect.addEventListener('change', () => {
                this.applyFormation(formationSelect.value);
            });
        }
        
        // Save button
        const saveButton = document.getElementById('save-formation');
        if (saveButton) {
            saveButton.addEventListener('click', () => {
                this.saveFormation();
            });
        }
    },
    
    loadTeamData() {
        fetch(`/api/formation/${this.teamId}`)
            .then(response => response.json())
            .then(data => {
                // Set formation selector to current formation
                const formationSelect = document.getElementById('formation');
                if (formationSelect) {
                    formationSelect.value = data.formation;
                }
                
                // Initialize players
                if (data.players && data.players.length > 0) {
                    // Team already has players with positions
                    this.players = data.players.map(player => ({
                        id: player.id,
                        name: player.name,
                        position: player.position,
                        x: player.x !== null ? player.x : (this.canvas.width * 0.3),
                        y: player.y !== null ? player.y : (this.canvas.height * 0.5),
                        radius: 15,
                        color: this.getPositionColor(player.position)
                    }));
                } else {
                    // Apply default formation
                    this.applyFormation(data.formation || '4-4-2');
                }
                
                // Initial draw
                this.draw();
            })
            .catch(error => {
                console.error('Error loading team data:', error);
                // Apply a default formation as fallback
                this.applyFormation('4-4-2');
                this.draw();
            });
    },
    
    applyFormation(formationName) {
        if (!this.formations[formationName]) {
            console.error('Formation not found:', formationName);
            return;
        }
        
        const template = this.formations[formationName];
        
        // If we already have players, just update their positions
        if (this.players.length > 0) {
            // Try to match players to positions intelligently
            template.forEach((slot, index) => {
                // Find existing player with this position or use index
                const existingPlayer = this.players.find(p => p.position === slot.position) || 
                                       (index < this.players.length ? this.players[index] : null);
                
                if (existingPlayer) {
                    existingPlayer.position = slot.position;
                    existingPlayer.x = slot.x * this.canvas.width;
                    existingPlayer.y = slot.y * this.canvas.height;
                    existingPlayer.color = this.getPositionColor(slot.position);
                }
            });
        } else {
            // Create placeholder players if none exist
            this.players = template.map((slot, index) => ({
                id: index + 1,
                name: `Player ${index + 1}`,
                position: slot.position,
                x: slot.x * this.canvas.width,
                y: slot.y * this.canvas.height,
                radius: 15,
                color: this.getPositionColor(slot.position)
            }));
        }
        
        this.draw();
    },
    
    setupEventListeners() {
        this.canvas.addEventListener('mousedown', this.handleMouseDown.bind(this));
        this.canvas.addEventListener('mousemove', this.handleMouseMove.bind(this));
        this.canvas.addEventListener('mouseup', this.handleMouseUp.bind(this));
        this.canvas.addEventListener('mouseout', this.handleMouseOut.bind(this));
    },
    
    handleMouseDown(event) {
        const mousePos = this.getMousePos(event);
        
        // Check if a player was clicked
        this.players.forEach(player => {
            const distance = Math.sqrt(
                Math.pow(player.x - mousePos.x, 2) + 
                Math.pow(player.y - mousePos.y, 2)
            );
            
            if (distance < player.radius) {
                this.selectedPlayer = player;
                this.isDragging = true;
            }
        });
        
        this.draw();
    },
    
    handleMouseMove(event) {
        if (!this.isDragging || !this.selectedPlayer) return;
        
        const mousePos = this.getMousePos(event);
        
        // Keep player within field boundaries
        this.selectedPlayer.x = Math.max(
            this.selectedPlayer.radius, 
            Math.min(mousePos.x, this.canvas.width - this.selectedPlayer.radius)
        );
        this.selectedPlayer.y = Math.max(
            this.selectedPlayer.radius, 
            Math.min(mousePos.y, this.canvas.height - this.selectedPlayer.radius)
        );
        
        this.draw();
    },
    
    handleMouseUp() {
        this.isDragging = false;
        this.selectedPlayer = null;
    },
    
    handleMouseOut() {
        this.isDragging = false;
        this.selectedPlayer = null;
    },
    
    getMousePos(event) {
        const rect = this.canvas.getBoundingClientRect();
        return {
            x: event.clientX - rect.left,
            y: event.clientY - rect.top
        };
    },
    
    draw() {
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw field
        this.drawField();
        
        // Draw players
        this.players.forEach(player => {
            this.drawPlayer(player);
        });
    },
    
    drawField() {
        // Field background
        this.ctx.fillStyle = '#4a8520';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Field outline
        this.ctx.strokeStyle = 'white';
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(10, 10, this.canvas.width - 20, this.canvas.height - 20);
        
        // Center line
        this.ctx.beginPath();
        this.ctx.moveTo(this.canvas.width / 2, 10);
        this.ctx.lineTo(this.canvas.width / 2, this.canvas.height - 10);
        this.ctx.stroke();
        
        // Center circle
        this.ctx.beginPath();
        this.ctx.arc(this.canvas.width / 2, this.canvas.height / 2, 40, 0, Math.PI * 2);
        this.ctx.stroke();
        
        // Penalty areas
        // Left penalty area
        const penAreaWidth = 80;
        const penAreaHeight = 150;
        this.ctx.strokeRect(
            10, 
            (this.canvas.height - penAreaHeight) / 2, 
            penAreaWidth, 
            penAreaHeight
        );
        
        // Right penalty area
        this.ctx.strokeRect(
            this.canvas.width - 10 - penAreaWidth, 
            (this.canvas.height - penAreaHeight) / 2, 
            penAreaWidth, 
            penAreaHeight
        );
        
        // Goal areas
        const goalAreaWidth = 30;
        const goalAreaHeight = 80;
        
        // Left goal area
        this.ctx.strokeRect(
            10, 
            (this.canvas.height - goalAreaHeight) / 2, 
            goalAreaWidth, 
            goalAreaHeight
        );
        
        // Right goal area
        this.ctx.strokeRect(
            this.canvas.width - 10 - goalAreaWidth, 
            (this.canvas.height - goalAreaHeight) / 2, 
            goalAreaWidth, 
            goalAreaHeight
        );
        
        // Corner arcs
        const cornerRadius = 10;
        
        // Top-left corner
        this.ctx.beginPath();
        this.ctx.arc(10, 10, cornerRadius, 0, Math.PI / 2);
        this.ctx.stroke();
        
        // Top-right corner
        this.ctx.beginPath();
        this.ctx.arc(this.canvas.width - 10, 10, cornerRadius, Math.PI / 2, Math.PI);
        this.ctx.stroke();
        
        // Bottom-left corner
        this.ctx.beginPath();
        this.ctx.arc(10, this.canvas.height - 10, cornerRadius, 0, -Math.PI / 2, true);
        this.ctx.stroke();
        
        // Bottom-right corner
        this.ctx.beginPath();
        this.ctx.arc(this.canvas.width - 10, this.canvas.height - 10, cornerRadius, -Math.PI / 2, -Math.PI, true);
        this.ctx.stroke();
    },
    
    drawPlayer(player) {
        // Player circle
        this.ctx.beginPath();
        this.ctx.arc(player.x, player.y, player.radius, 0, Math.PI * 2);
        this.ctx.fillStyle = player.color;
        this.ctx.fill();
        this.ctx.lineWidth = 2;
        this.ctx.strokeStyle = 'white';
        this.ctx.stroke();
        
        // Position label
        this.ctx.font = '10px Arial';
        this.ctx.fillStyle = 'white';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText(player.position, player.x, player.y);
        
        // Player name (below the circle)
        this.ctx.font = '9px Arial';
        this.ctx.fillText(player.name, player.x, player.y + player.radius + 10, player.radius * 4);
    },
    
    getPositionColor(position) {
        // Color coding by position type
        const positionColors = {
            'GK': '#ffcc00', // Yellow
            'CB': '#0066cc', // Blue
            'LB': '#0099cc', // Light Blue
            'RB': '#0099cc', // Light Blue
            'LWB': '#33cccc', // Teal
            'RWB': '#33cccc', // Teal
            'DM': '#339933', // Green
            'CM': '#33cc33', // Light Green
            'LM': '#66cc33', // Lime
            'RM': '#66cc33', // Lime
            'AM': '#cc9933', // Orange
            'LW': '#cc6633', // Brown
            'RW': '#cc6633', // Brown
            'CF': '#cc3333', // Red
            'ST': '#cc3333'  // Red
        };
        
        return positionColors[position] || '#999999'; // Default gray for unknown positions
    },
    
    saveFormation() {
        // Prepare players data
        const playersData = this.players.map(player => ({
            id: player.id,
            position: player.position,
            x: player.x,
            y: player.y
        }));
        
        // Get formation value from select
        const formationSelect = document.getElementById('formation');
        const formation = formationSelect ? formationSelect.value : '4-4-2';
        
        // Send to server
        fetch(`/api/formation/${this.teamId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                formation: formation,
                players: playersData
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Show success message
                const messageElement = document.getElementById('save-message');
                if (messageElement) {
                    messageElement.textContent = 'Formation saved successfully!';
                    messageElement.style.color = 'green';
                    setTimeout(() => {
                        messageElement.textContent = '';
                    }, 3000);
                } else {
                    alert('Formation saved successfully!');
                }
            } else {
                throw new Error('Failed to save formation');
            }
        })
        .catch(error => {
            console.error('Error saving formation:', error);
            alert('Error saving formation. Please try again.');
        });
    }
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Check if we're on the formation page
    const canvas = document.getElementById('formation-canvas');
    if (canvas) {
        const teamId = canvas.getAttribute('data-team-id');
        if (teamId) {
            formationEditor.initialize('formation-canvas', teamId);
        } else {
            console.error('Team ID not specified');
        }
    }
});