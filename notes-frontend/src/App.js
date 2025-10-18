import React, { useState } from "react";

function App() {
  const [username, setUsername] = useState("");      // state to store input
  const [notes, setNotes] = useState([]);            // state to store notes

  const fetchNotes = async () => {
    try {
      const res = await fetch(`http://localhost:8000/users/by-username/${username}`, {
        headers: {
          "X-API-Key": "supersecretkey123",          // use your backend API key
        },
      });

      if (!res.ok) {
        throw new Error("User not found");
      }

      const user = await res.json();

      const notesRes = await fetch(`http://localhost:8000/users/${user.id}/notes/`, {
        headers: {
          "X-API-Key": "supersecretkey123",
        },
      });

      const notesData = await notesRes.json();
      setNotes(notesData);
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <div>
      <h1>Notes App</h1>

      <input
        type="text"
        placeholder="Enter username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <button onClick={fetchNotes}>Get Notes</button>

      <ul>
        {notes.map((note) => (
          <li key={note.id}>
            <strong>{note.title}</strong>: {note.content}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
