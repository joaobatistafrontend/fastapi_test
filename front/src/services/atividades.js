import api from "./api";

export function getAtividade(id) {
  return api.get(`/atividades/${id}`);
}

export function updateAtividade(id, data) {
  return api.put(`/atividades/${id}`, data);
}

export function deleteAtividade(id) {
  return api.delete(`/atividades/${id}`);
}
