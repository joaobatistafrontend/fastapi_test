import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import ActivityDetail from "./components/ActivityDetail";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/atividades/:id" element={<ActivityDetail />} />
    </Routes>
  );
}
