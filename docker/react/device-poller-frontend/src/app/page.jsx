export default async function HomePage() {
  const response = await fetch("http://127.0.0.1:5000/devices", {
    cache: "no-store",
  }); // Prevent caching if you need fresh data
  const data = await response.json();
  const devices = JSON.parse(data.device_list);

  return (
    <div>
      <DeviceTable devices={devices} />
    </div>
  );
}

function DeviceTable({ devices }) {
  return (
    <table>
      <thead>
        <tr>
          <td>Device Name</td>
          <td>Device IP</td>
          <td>Edit</td>
        </tr>
      </thead>
      <tbody>
        {devices.map((device) => (
          <tr key={device._id}>
            <td>{device._id}</td>
            <td>{device.testInsert}</td>
            <td>
              <button>Edit</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
