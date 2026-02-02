import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../services/api";

export default function AtividadeDetalhe() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [atividade, setAtividade] = useState({
    titulo: "",
    descricao: "",
    status: "",
    img_path: "",
  });

  const [imagem, setImagem] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(true);

  // 🔹 GET atividade
  useEffect(() => {
    api.get(`/atividades/${id}`)
      .then(res => {
        setAtividade(res.data);
        if (res.data.img_path) {
          setPreview(`http://localhost:8000/${res.data.img_path}`);
        }
        setLoading(false);
      })
      .catch(() => {
        alert("Atividade não encontrada");
        navigate("/");
      });
  }, [id, navigate]);

  // 🔹 PUT atividade (FORMDATA)
  async function handleUpdate(e) {
    e.preventDefault();

    try {
      const formData = new FormData();
      formData.append("titulo", atividade.titulo);
      formData.append("descricao", atividade.descricao || "");
      formData.append("status", atividade.status);

      if (imagem) {
        formData.append("imagem", imagem);
      }

      await api.put(`/atividades/${id}`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      alert("Atividade atualizada com sucesso!");
    } catch (error) {
      console.error(error.response?.data || error);
      alert("Erro ao atualizar atividade");
    }
  }

  // 🔹 DELETE
  async function handleDelete() {
    if (!window.confirm("Tem certeza que deseja deletar?")) return;

    try {
      await api.delete(`/atividades/${id}`);
      alert("Atividade deletada com sucesso!");
      navigate("/");
    } catch {
      alert("Erro ao deletar atividade");
    }
  }

  if (loading) {
    return <p className="text-center mt-10">Carregando...</p>;
  }

  return (
    <div className="max-w-xl mx-auto mt-10 p-6 bg-white shadow rounded">
      <h1 className="text-2xl font-bold mb-4">Editar Atividade</h1>

      <form onSubmit={handleUpdate} className="space-y-4">
        <input
          type="text"
          className="w-full border p-2 rounded"
          value={atividade.titulo}
          onChange={e =>
            setAtividade({ ...atividade, titulo: e.target.value })
          }
        />

        <textarea
          className="w-full border p-2 rounded"
          value={atividade.descricao}
          onChange={e =>
            setAtividade({ ...atividade, descricao: e.target.value })
          }
        />

        <select
          className="w-full border p-2 rounded"
          value={atividade.status}
          onChange={e =>
            setAtividade({ ...atividade, status: e.target.value })
          }
        >
          <option value="PENDENTE">Pendente</option>
          <option value="EM_ANDAMENTO">Em andamento</option>
          <option value="CONCLUIDA">Concluída</option>
        </select>

        {/* 🔹 Upload REAL */}
        <input
          type="file"
          accept="image/*"
          onChange={(e) => {
            const file = e.target.files[0];
            setImagem(file);
            if (file) {
              setPreview(URL.createObjectURL(file));
            }
          }}
        />

        {/* 🔹 Preview */}
        {preview && (
          <img
            src={preview}
            className="w-full h-40 object-cover rounded"
          />
        )}

        <div className="flex gap-4">
          <button className="flex-1 bg-blue-600 text-white py-2 rounded">
            Salvar
          </button>

          <button
            type="button"
            onClick={handleDelete}
            className="flex-1 bg-red-600 text-white py-2 rounded"
          >
            Deletar
          </button>
        </div>
      </form>
    </div>
  );
}
