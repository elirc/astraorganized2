// Synthetic encryption for tests only. This is not an OS credential vault.
module.exports = {
  isEncryptionAvailable: () => true,
  encryptString: (text) => Buffer.from("test-fixture:" + text),
  decryptString: (bytes) => {
    const text = bytes.toString();
    if (!text.startsWith("test-fixture:"))
      throw new Error("Invalid synthetic encrypted value");
    return text.slice("test-fixture:".length);
  },
};
