import express from "express";
import cors from "cors";
import sharp from "sharp";

const app = express();
app.use(cors());
app.use(express.json({ limit: "10mb" }));

app.post("/decode-image", async (req, res) => {
  try {
    const base64Data = req.body.base64;
    const buffer = Buffer.from(base64Data.split(",")[1], "base64");

    const { data, info } = await sharp(buffer)
      .raw()
      .ensureAlpha() // rgba
      .toBuffer({ resolveWithObject: true });

    res.json({
      width: info.width,
      height: info.height,
      pixels: Array.from(data), // envia como array de bytes
    });
  } catch (e) {
    console.error(e);
    res.status(500).send("Erro ao processar imagem");
  }
});

app.listen(3000, () => {
  console.log("Servidor rodando na porta 3000");
});
