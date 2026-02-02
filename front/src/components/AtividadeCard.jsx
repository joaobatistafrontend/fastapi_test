import { Link } from "react-router-dom";

export default function AtividadeCard({ atividade }) {
  const statusColor = {
    PENDENTE: "bg-yellow-100 text-yellow-800",
    EM_ANDAMENTO: "bg-blue-100 text-blue-800",
    CONCLUIDA: "bg-green-100 text-green-800",
  };

  return (
    <Link
      to={`/atividades/${atividade.id}`}
      className="block bg-white p-4 rounded-xl shadow hover:shadow-lg transition"
    >
      <span className="text-sm text-gray-500">
        ID: {atividade.id}
      </span>

      <h3 className="font-semibold text-lg">
        {atividade.titulo}
      </h3>

      {atividade.descricao && (
        <p className="text-gray-600 text-sm mt-1">
          {atividade.descricao}
        </p>
      )}

      <span
        className={`inline-block mt-3 px-3 py-1 text-sm rounded-full ${statusColor[atividade.status]}`}
      >
        {atividade.status}
      </span>
    </Link>
  );
}
