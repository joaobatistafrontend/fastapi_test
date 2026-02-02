import { useState } from "react";
import api from "../services/api";

export default function AtividadeForm({ onSuccess }) {
  const [titulo, setTitulo] = useState("");
  const [descricao, setDescricao] = useState("");
  const [status, setStatus] = useState("PENDENTE");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);

    try {
      await api.post("/atividades/criar_atividade", {
        titulo,
        descricao,
        status,
        img_path: null,
      });

      setTitulo("");
      setDescricao("");
      setStatus("PENDENTE");
      onSuccess(); // recarrega lista
    } catch (err) {
      alert("Erro ao salvar atividade");
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white p-6 rounded-xl shadow-md space-y-4"
    >
      <h2 className="text-xl font-bold text-gray-700">
        Nova Atividade
      </h2>

      <input
        className="w-full border rounded-lg p-2 focus:outline-none focus:ring"
        placeholder="Título"
        value={titulo}
        onChange={(e) => setTitulo(e.target.value)}
        required
      />

      <textarea
        className="w-full border rounded-lg p-2 focus:outline-none focus:ring"
        placeholder="Descrição"
        value={descricao}
        onChange={(e) => setDescricao(e.target.value)}
      />

      <select
        className="w-full border rounded-lg p-2"
        value={status}
        onChange={(e) => setStatus(e.target.value)}
      >
        <option value="PENDENTE">Pendente</option>
        <option value="EM_ANDAMENTO">Em andamento</option>
        <option value="CONCLUIDA">Concluída</option>
      </select>

      <button
        disabled={loading}
        className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
      >
        {loading ? "Salvando..." : "Salvar"}
      </button>
    </form>
  );
}
