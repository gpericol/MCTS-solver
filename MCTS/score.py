
class Score():
    @staticmethod
    def _bitcount(v):
        return bin(v).count("1")

    @staticmethod
    def _leading_zeros(v, bitsize):
        # padd bit string
        s = format(v, "0{}b".format(bitsize))

        return len(s) - len(s.lstrip('0'))

    @staticmethod
    def _trailing_zeros(v, bitsize):
        # padd bit string
        s = format(v, "0{}b".format(bitsize))

        return len(s) - len(s.rstrip('0'))

    @staticmethod
    def _leading_ones(v, bitsize):
        # padd bit string
        s = format(v, "0{}b".format(bitsize))

        return len(s) - len(s.lstrip('1'))

    @staticmethod
    def _trailing_ones(v, bitsize):
        # padd bit string
        s = format(v, "0{}b".format(bitsize))

        return len(s) - len(s.rstrip('1'))

    @staticmethod
    def _num_distance(a, b):
        return abs(a - b)

    @staticmethod
    def _rotate_left(a, b, size):
        shift = b & (size - 1)
        return ((a << shift) | (a >> size - shift)) % 2 ** size

    @staticmethod
    def _metric_hamming_distance(a, b, bitsize):
        n = Score._bitcount(a ^ b)
        return 1 - (n / bitsize)

    @staticmethod
    def _metric_leading_zeros(a, b, bitsize):
        # leading zeros
        a = Score._leading_zeros(a, bitsize)
        b = Score._leading_zeros(b, bitsize)

        # numeric difference
        n = abs(a - b)

        return 1 - float(n / bitsize)

    @staticmethod
    def _metric_trailing_zeros(a, b, bitsize):
        # leading zeros
        a = Score._trailing_zeros(a, bitsize)
        b = Score._trailing_zeros(b, bitsize)

        # numeric difference
        n = abs(a - b)

        return 1 - float(n / bitsize)

    @staticmethod
    def _metric_leading_ones(a, b, bitsize):
        # leading ones
        a = Score._leading_ones(a, bitsize)
        b = Score._leading_ones(b, bitsize)

        # numeric difference
        n = abs(a - b)

        return 1 - float(n / bitsize)

    @staticmethod
    def _metric_trailing_ones(a, b, bitsize):
        # trailing ones
        a = Score._trailing_ones(a, bitsize)
        b = Score._trailing_ones(b, bitsize)

        # numeric difference
        n = abs(a - b)

        return 1 - float(n / bitsize)

    @staticmethod
    def _metric_num_distance(a, b):
        # numeric distance
        d = Score._num_distance(a, b)

        # avoid division by 0
        if a == b:
            return 1
        else:
            # maximum of a and b
            maximum = max([abs(a), abs(b)])
            return 1 - (d / maximum)

    @staticmethod
    def distance_metric(a, b, bitsize):
        # initial score
        score = 0.0

        # apply metrics
        for x, y in [(a, b)]:
            score += Score._metric_hamming_distance(x, y, bitsize)
            score += Score._metric_leading_zeros(x, y, bitsize)
            score += Score._metric_trailing_zeros(x, y, bitsize)
            score += Score._metric_leading_ones(x, y, bitsize)
            score += Score._metric_trailing_ones(x, y, bitsize)
            score += Score._metric_num_distance(x, y)

        # normalise weights
        d = score / 6

        return d