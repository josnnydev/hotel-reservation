export async function login(username: string, password: string): Promise<string | null> {
    const res = await fetch("http://localhost:8000/api-token-auth/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (!res.ok) return null;
    const data = await res.json();
    return data.token;
  }
  
  export const createReserva = async (token: string, reserva: any): Promise<boolean> => {
    try {
      const response = await fetch("http://localhost:8000/api/create-reservation/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${token}`,
        },
        body: JSON.stringify(reserva),
      });
  
      if (!response.ok) {
        throw new Error('Error al crear la reserva');
      }
  
      const data = await response.json();
      return data.message === 'Room disabled successfully';  // Ajusta la validación si es necesario
    } catch (error) {
      console.error(error);
      return false;
    }
  };
  

  export async function getHotelsRoomsBuses(token: string): Promise<any> {
    const res = await fetch("http://localhost:8000/api/get-hotels-rooms-buses/", {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
    });
    return await res.json();
  }
  

  