import numpy as np
import pytest

from edge.features import normalize_landmarks


def make_hand(offset=(0.0, 0.0, 0.0), scale=1.0, seed=0):
    rng = np.random.default_rng(seed)
    pts = rng.uniform(0.0, 0.2, size=(21, 3)).astype(np.float32)
    pts[0] = 0.0  # pulso na origem
    return pts * scale + np.array(offset, dtype=np.float32)


def test_shape():
    assert normalize_landmarks(make_hand()).shape == (63,)


def test_invariante_a_posicao():
    a = normalize_landmarks(make_hand())
    b = normalize_landmarks(make_hand(offset=(0.5, 0.3, 0.1)))
    np.testing.assert_allclose(a, b, atol=1e-5)


def test_invariante_a_escala():
    a = normalize_landmarks(make_hand())
    b = normalize_landmarks(make_hand(scale=2.5))
    np.testing.assert_allclose(a, b, atol=1e-5)


def test_pulso_na_origem_e_escala_unitaria():
    v = normalize_landmarks(make_hand(offset=(0.3, 0.3, 0.0))).reshape(21, 3)
    np.testing.assert_allclose(v[0], 0.0, atol=1e-6)
    assert np.isclose(np.max(np.linalg.norm(v, axis=1)), 1.0)


def test_forma_errada():
    with pytest.raises(ValueError):
        normalize_landmarks(np.zeros((20, 3)))


def test_degenerado():
    with pytest.raises(ValueError):
        normalize_landmarks(np.zeros((21, 3)))
