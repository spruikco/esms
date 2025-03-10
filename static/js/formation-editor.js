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