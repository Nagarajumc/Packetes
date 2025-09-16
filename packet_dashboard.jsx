import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
import { useEffect, useState } from "react";

export default function Dashboard() {
  const [stats, setStats] = useState({ packets: 0, connections: 0, errors: 0, alerts: 0 });
  const [lineData, setLineData] = useState([]);
  const [pieData, setPieData] = useState([]);
  const [tableData, setTableData] = useState([]);

  useEffect(() => {
    // Mock Data (replace with API fetch for real backend)
    setStats({ packets: 15234, connections: 45, errors: 3, alerts: 5 });

    setLineData([
      { time: "10:00", count: 200 },
      { time: "10:05", count: 400 },
      { time: "10:10", count: 350 },
      { time: "10:15", count: 500 },
      { time: "10:20", count: 700 },
    ]);

    setPieData([
      { protocol: "TCP", value: 60 },
      { protocol: "UDP", value: 25 },
      { protocol: "ICMP", value: 10 },
      { protocol: "Other", value: 5 },
    ]);

    setTableData([
      { src: "192.168.1.10", dst: "10.0.0.5", protocol: "TCP", size: "512B", time: "10:20:15" },
      { src: "192.168.1.12", dst: "10.0.0.8", protocol: "UDP", size: "256B", time: "10:20:20" },
      { src: "192.168.1.14", dst: "10.0.0.9", protocol: "ICMP", size: "128B", time: "10:20:25" },
      { src: "192.168.1.15", dst: "10.0.0.11", protocol: "TCP", size: "1KB", time: "10:20:30" },
    ]);
  }, []);

  const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      {/* Header */}
      <div className="bg-blue-900 text-white text-2xl font-bold p-4 rounded-2xl shadow mb-6">
        Packet Monitoring Dashboard
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <Card className="shadow-lg rounded-2xl">
          <CardContent className="p-4">
            <p className="text-gray-500">Packets Captured</p>
            <h2 className="text-2xl font-bold">{stats.packets}</h2>
          </CardContent>
        </Card>
        <Card className="shadow-lg rounded-2xl">
          <CardContent className="p-4">
            <p className="text-gray-500">Active Connections</p>
            <h2 className="text-2xl font-bold">{stats.connections}</h2>
          </CardContent>
        </Card>
        <Card className="shadow-lg rounded-2xl">
          <CardContent className="p-4">
            <p className="text-gray-500">Errors</p>
            <h2 className="text-2xl font-bold text-red-600">{stats.errors}</h2>
          </CardContent>
        </Card>
        <Card className="shadow-lg rounded-2xl">
          <CardContent className="p-4">
            <p className="text-gray-500">Alerts</p>
            <h2 className="text-2xl font-bold text-yellow-600">{stats.alerts}</h2>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <Card className="col-span-2 shadow-lg rounded-2xl">
          <CardContent className="p-4">
            <h3 className="font-semibold mb-2">Packets Over Time</h3>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={lineData}>
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="count" stroke="#8884d8" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card className="shadow-lg rounded-2xl">
          <CardContent className="p-4">
            <h3 className="font-semibold mb-2">Protocol Distribution</h3>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie data={pieData} dataKey="value" nameKey="protocol" cx="50%" cy="50%" outerRadius={80} label>
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Table */}
      <Card className="shadow-lg rounded-2xl">
        <CardContent className="p-4">
          <h3 className="font-semibold mb-2">Recent Packets</h3>
          <div className="overflow-x-auto">
            <table className="table-auto w-full border-collapse">
              <thead>
                <tr className="bg-gray-100 text-left">
                  <th className="p-2">Source IP</th>
                  <th className="p-2">Destination IP</th>
                  <th className="p-2">Protocol</th>
                  <th className="p-2">Size</th>
                  <th className="p-2">Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {tableData.map((pkt, idx) => (
                  <tr key={idx} className="border-b">
                    <td className="p-2">{pkt.src}</td>
                    <td className="p-2">{pkt.dst}</td>
                    <td className="p-2">{pkt.protocol}</td>
                    <td className="p-2">{pkt.size}</td>
                    <td className="p-2">{pkt.time}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
