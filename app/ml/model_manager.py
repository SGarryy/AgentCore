"""Secure model loading and management."""

import logging
import hashlib
import hmac
from pathlib import Path
from typing import Any
import joblib

logger = logging.getLogger(__name__)


class SecurityError(Exception):
    """Security validation failed."""

    pass


class MissingSignatureError(SecurityError):
    """Model signature file is required but missing."""

    pass


class ModelManager:
    """Manages model loading with integrity checks."""

    def __init__(self, model_path: Path, signature_path: Path):
        """
        Initialize model manager.

        Args:
            model_path: Path to model file
            signature_path: Path to model signature file
        """
        self.model_path = Path(model_path)
        self.signature_path = Path(signature_path)
        self._model = None

    def verify_integrity(self) -> bool:
        """
        Verify model hasn't been tampered with.

        Returns:
            True if model is valid

        Raises:
            FileNotFoundError: If model not found
            SecurityError: If integrity check fails
        """
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found: {self.model_path}")

        if not self.signature_path.exists():
            raise MissingSignatureError(f"No signature file found for model: {self.signature_path}")

        # Calculate hash of model file
        sha256_hash = hashlib.sha256()
        with open(self.model_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)

        calculated_hash = sha256_hash.hexdigest()

        # Read expected hash
        with open(self.signature_path, "r") as f:
            expected_hash = f.read().strip()

        # Constant-time comparison to prevent timing attacks
        if not hmac.compare_digest(calculated_hash, expected_hash):
            raise SecurityError("Model integrity check failed - file may be corrupted or tampered")

        logger.info("Model integrity verified")
        return True

    def load(self, force_reload: bool = False) -> Any:
        """
        Load model with integrity checks.

        Args:
            force_reload: Force reload even if cached

        Returns:
            Loaded model object

        Raises:
            FileNotFoundError: If model not found
            SecurityError: If integrity check fails
        """
        if self._model is not None and not force_reload:
            logger.debug("Using cached model")
            return self._model

        try:
            self.verify_integrity()
            logger.info(f"Loading model from {self.model_path}")
            self._model = joblib.load(self.model_path)
            logger.info("Model loaded successfully")
            return self._model
        except Exception as e:
            logger.error(f"Failed to load model: {e}", exc_info=True)
            raise

    def save(self, model: Any, create_signature: bool = True) -> None:
        """
        Save model with optional integrity signature.

        Args:
            model: Model to save
            create_signature: Create integrity signature file

        Raises:
            IOError: If save fails
        """
        try:
            self.model_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Saving model to {self.model_path}")
            joblib.dump(model, self.model_path)

            if create_signature:
                # Calculate and save hash
                sha256_hash = hashlib.sha256()
                with open(self.model_path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        sha256_hash.update(chunk)

                with open(self.signature_path, "w") as f:
                    f.write(sha256_hash.hexdigest())
                logger.info(f"Model signature created: {self.signature_path}")
        except Exception as e:
            logger.error(f"Failed to save model: {e}", exc_info=True)
            raise
