import { useEffect, useState } from "react";
import api from "../services/api";
import AtividadeCard from "./AtividadeCard";

export default function AtividadeList({ reload }) {
  const [atividades, setAtividades] = useState([]);
  const [loading, setLoading] = useState(true);

  async function carregar() {
    try {
      const response = await api.get("/atividades/listar");
      setAtividades(response.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    carregar();
  }, [reload]);

  if (loading) return <p>Carregando...</p>;

  return (
    <div className="grid md:grid-cols-2 gap-4">
      {atividades.map((atividade) => (
        <AtividadeCard
          key={atividade.id}
          atividade={atividade}
        />
      ))}
    </div>
  );
}
