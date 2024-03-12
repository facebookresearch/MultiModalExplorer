export const getEmbeddingPoints = async (): Promise<[number, number][]> => {
  return new Promise((resolve, reject) => {
    try {
      setTimeout(() => {
        const embeddings: [number, number][] = new Array(10000)
          .fill(null)
          .map(() => [-1 + Math.random() * 2, -1 + Math.random() * 2]);
        resolve(embeddings);
      }, 5000);
    } catch (error) {
      console.log(error);
      reject(error);
    }
  });
};
