import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import FormationEditor from '../components/formation/FormationEditor';

// Import your database/API service
// import { getTeamById, getPlayersByTeamId, saveFormation, getFormationByTeamId } from '../services/api';

const TeamFormationPage = () => {
  const { teamId } = useParams();
  const navigate = useNavigate();
  
  const [team, setTeam] = useState(null);
  const [players, setPlayers] = useState([]);
  const [formation, setFormation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch team details
        // const teamData = await getTeamById(teamId);
        // setTeam(teamData);
        
        // For demonstration, using mock data
        setTeam({
          id: teamId,
          name: 'Demo Team',
          logo: 'https://via.placeholder.com/150'
        });
        
        // Fetch players
        // const playersData = await getPlayersByTeamId(teamId);
        // setPlayers(playersData);
        
        // For demonstration, using mock data
        setPlayers([
          { id: 'p1', name: 'John Smith', number: 1, position: 'Goalkeeper' },
          { id: 'p2', name: 'David Jones', number: 2, position: 'Defender' },
          { id: 'p3', name: 'Michael Brown', number: 3, position: 'Defender' },
          { id: 'p4', name: 'Robert Wilson', number: 4, position: 'Defender' },
          { id: 'p5', name: 'James Taylor', number: 5, position: 'Defender' },
          { id: 'p6', name: 'William Davis', number: 6, position: 'Midfielder' },
          { id: 'p7', name: 'Richard Miller', number: 7, position: 'Midfielder' },
          { id: 'p8', name: 'Joseph Allen', number: 8, position: 'Midfielder' },
          { id: 'p9', name: 'Thomas Young', number: 9, position: 'Midfielder' },
          { id: 'p10', name: 'Charles King', number: 10, position: 'Forward' },
          { id: 'p11', name: 'Daniel Scott', number: 11, position: 'Forward' },
          { id: 'p12', name: 'Matthew Green', number: 12, position: 'Goalkeeper' },
          { id: 'p13', name: 'Anthony Baker', number: 13, position: 'Defender' },
          { id: 'p14', name: 'Donald Nelson', number: 14, position: 'Midfielder' },
          { id: 'p15', name: 'Mark Carter', number: 15, position: 'Forward' }
        ]);
        
        // Fetch existing formation if any
        // const formationData = await getFormationByTeamId(teamId);
        // setFormation(formationData);
        
        // For demonstration, no initial formation
        setFormation(null);
        
        setLoading(false);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('Failed to load team data');
        setLoading(false);
      }
    };
    
    fetchData();
  }, [teamId]);
  
  const handleSaveFormation = async (formationData) => {
    try {
      // Save formation to database/API
      // await saveFormation(formationData);
      
      // For demonstration
      console.log('Formation saved:', formationData);
      alert('Formation saved successfully!');
      
      // Optionally navigate back to team page
      // navigate(`/teams/${teamId}`);
    } catch (err) {
      console.error('Error saving formation:', err);
      alert('Error saving formation. Please try again.');
    }
  };
  
  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        <p>{error}</p>
        <button 
          className="mt-2 bg-red-500 text-white px-4 py-2 rounded"
          onClick={() => navigate('/teams')}
        >
          Back to Teams
        </button>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto px-4 py-6">
      <div className="flex justify-between items-center mb-6">
        <div className="flex items-center">
          <h1 className="text-2xl font-bold">{team.name} - Formation</h1>
        </div>
        <button
          className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
          onClick={() => navigate(`/teams/${teamId}`)}
        >
          Back to Team
        </button>
      </div>
      
      <FormationEditor 
        players={players}
        initialFormation={formation}
        onSave={handleSaveFormation}
        teamId={teamId}
      />
    </div>
  );
};

export default TeamFormationPage;