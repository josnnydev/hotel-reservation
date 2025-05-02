import { createReserva, getHotelsRoomsBuses } from "./api/api";

const reservaForm = document.getElementById("reserva-form") as HTMLFormElement;
const message = document.getElementById("message")!;

const hotelSelect = document.getElementById("hotel") as HTMLSelectElement;
const roomSelect = document.getElementById("room") as HTMLSelectElement;
const busSelect = document.getElementById("bus") as HTMLSelectElement;

const token = localStorage.getItem("token");
if (!token) window.location.href = "/login.html";

// Cargar hoteles, habitaciones y buses
(async () => {
  const data = await getHotelsRoomsBuses(token!);

  // Acceder a los datos específicos de hoteles, habitaciones y autobuses
  const hotels = data.hotels;
  const rooms = data.rooms;
  const buses = data.buses;

  // Poblar el select de hoteles
  hotels.forEach((hotel: any) => {
    const option = document.createElement("option");
    option.value = hotel.id;
    option.textContent = hotel.name;
    hotelSelect.appendChild(option);
  });

  // Poblar el select de habitaciones
  rooms.forEach((room: any) => {
    const option = document.createElement("option");
    option.value = room.id;
    option.textContent = `${room.type_room} - $${room.price_room}`;
    roomSelect.appendChild(option);
  });

  // Poblar el select de autobuses
  buses.forEach((bus: any) => {
    const option = document.createElement("option");
    option.value = bus.id;
    option.textContent = `${bus.name} (${bus.capacity} plazas) - $${bus.price_bus}`;
    busSelect.appendChild(option);
  });
})();

reservaForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const reserva = {
    hotel: hotelSelect.value,
    type_room: roomSelect.value,
    name: busSelect.value,
    check_in: (document.getElementById("check_in") as HTMLInputElement).value,
    check_out: (document.getElementById("check_out") as HTMLInputElement).value,
    price: parseFloat((document.getElementById("price") as HTMLInputElement).value),
  };

  const success = await createReserva(token!, reserva);
  message.textContent = success
    ? "✅ Reserva creada correctamente"
    : "❌ Error al crear la reserva";
});
